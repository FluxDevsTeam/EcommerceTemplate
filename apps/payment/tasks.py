from django.core.mail import mail_admins
from django.conf import settings

from .serializers import PaymentCartSerializer
from ..orders.models import Order, OrderItem
from ..cart.models import Cart
from decimal import Decimal
from django.db import transaction
from django.db.utils import OperationalError
from .emails import order_confirmation_email
from celery import shared_task, current_app
from celery.exceptions import MaxRetriesExceededError
import logging

logger = logging.getLogger(__name__)


def is_celery_healthy():
    try:
        current_app.connection().ensure_connection(max_retries=0)
        return True
    except Exception as e:
        logger.error(f"Celery broker is not healthy: {str(e)}")
        return False


def send_email_synchronously(order_id, user_email, first_name, total_amount, order_date, estimated_delivery):

    try:
        order_confirmation_email(
            order_id=order_id,
            user_email=user_email,
            first_name=first_name,
            total_amount=total_amount,
            order_date=order_date,
            estimated_delivery=estimated_delivery
        )

        logger.info(f"Synchronously sent order confirmation email for order {order_id} to {user_email}")
        return {"status": "success", "order_id": order_id, "email": user_email}
    except Exception as e:
        logger.exception(
            "Failed to send order confirmation email synchronously",
            extra={'order_id': order_id, 'user_email': user_email, 'error': str(e)}
        )
        return {"status": "failure", "order_id": order_id, "email": user_email, "error": str(e)}


@shared_task(bind=True, max_retries=3)
def send_order_confirmation_email(self, order_id, user_email, first_name, total_amount, order_date, estimated_delivery):

    try:
        order_confirmation_email(
            order_id=order_id,
            user_email=user_email,
            first_name=first_name,
            total_amount=total_amount,
            order_date=order_date,
            estimated_delivery=estimated_delivery
        )

        logger.info(f"Sent order confirmation email for order {order_id} to {user_email} via Celery")
        return {"status": "success", "order_id": order_id, "email": user_email}
    except Exception as e:
        logger.exception(
            "Failed to send order confirmation email via Celery",
            extra={'order_id': order_id, 'user_email': user_email, 'error': str(e)}
        )
        try:
            self.retry(exc=e, countdown=30)
        except MaxRetriesExceededError:
            logger.warning(f"Max retries exceeded for order {order_id}. Falling back to synchronous email sending.")
            return send_email_synchronously(order_id, user_email, first_name, total_amount)


@shared_task(bind=True, max_retries=3)
def create_order_from_webhook(self, user_id, cart_id, tx_ref, provider, amount, email):
    try:
        with transaction.atomic():
            user = settings.AUTH_USER_MODEL.objects.get(id=user_id)
            cart = Cart.objects.get(id=cart_id, user=user)

        for item in cart.cartitem_cart.all():
            product = item.product
            if product.stock < item.quantity:
                logger.warning("Insufficient stock in webhook task",
                               extra={'product_id': product.id, 'user_id': user_id})
                raise ValueError(f"Insufficient stock for {product.name}")
            if product.price != item.product.price:
                logger.warning("Price changed in webhook task",
                               extra={'product_id': product.id, 'user_id': user_id})
                raise ValueError("Product prices have changed")

        serializer = PaymentCartSerializer(cart)
        server_total = serializer.data["total"]
        if abs(Decimal(str(server_total)) - Decimal(str(amount))) > Decimal("0.01"):
            logger.error("Webhook amount mismatch in task",
                         extra={'server_total': server_total, 'amount': amount, 'tx_ref': tx_ref})
            raise ValueError("Amount mismatch")

        order = Order.objects.create(
            user=user,
            status="Paid",
            delivery_fee=cart.delivery_fee,
            total_amount=server_total,
            first_name=cart.first_name or user.first_name,
            last_name=cart.last_name or user.last_name,
            email=cart.email or user.email,
            state=cart.state,
            city=cart.city,
            delivery_address=cart.delivery_address,
            phone_number=cart.phone_number or user.phone_number,
            transaction_id=tx_ref,
            payment_provider=provider,
            estimated_delivery=cart.estimated_delivery
        )

        for item in cart.cartitem_cart.all():
            product = item.product
            product.stock -= item.quantity
            product.save()
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item.quantity,
                name=product.name,
                description=product.description,
                colour="N/A",
                image1=product.image1,
                price=product.price,
                size=item.size.name
            )

        cart.cartitem_cart.all().delete()
        logger.info(f"Order {order.id} created via webhook task",
                    extra={'provider': provider, 'tx_ref': tx_ref, 'user_id': user_id})

        send_order_confirmation_email.delay(
            order_id=str(order.id),
            user_email=order.email,
            first_name=order.first_name,
            total_amount=str(order.total_amount)
        )

    except (OperationalError, ValueError) as e:
        logger.exception("Failed to create order in webhook task",
                         extra={'tx_ref': tx_ref, 'user_id': user_id, 'error': str(e)})
        try:
            self.retry(exc=e, countdown=60 * (self.request.retries + 1))
        except self.MaxRetriesExceededError:
            logger.error("Max retries exceeded for order creation",
                         extra={'tx_ref': tx_ref, 'user_id': user_id})
            subject = f"🚨 CRITICAL: Order Creation Failed (TX: {tx_ref})"
            message = f"""
            Failed to create order after multiple retries!

            Transaction Details:
            - Reference: {tx_ref}
            - Payment Provider: {provider}
            - Amount: {amount} {settings.PAYMENT_CURRENCY}

            User Details:
            - ID: {user_id}
            - Email: {email}

            Error Details:
            {str(e)}

            Immediate manual intervention required!
            """
            try:
                mail_admins(
                    subject=subject,
                    message=message,
                    fail_silently=False
                )
                logger.info("Admin notification sent for failed order",
                            extra={'tx_ref': tx_ref, 'user_id': user_id})
            except Exception as mail_error:
                logger.critical("Failed to send admin notification",
                                extra={'tx_ref': tx_ref,
                                       'error': str(mail_error),
                                       'original_error': str(e)})
