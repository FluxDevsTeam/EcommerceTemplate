from drf_yasg.utils import swagger_auto_schema
from .pagination import PAGINATION_PARAMS
from django.conf import settings
import requests
from django.utils import timezone
from .tasks import (send_refund_initiated_notification_email, is_celery_healthy, send_refund_initiated_email_synchronously,
                    refund_confirmation_email, send_order_shipped_email, send_order_delivered_email,
                    send_shipped_email_synchronously, send_delivered_email_synchronously)
from django.utils.functional import SimpleLazyObject
from ..ecommerce_admin.models import OrganizationSettings, DeveloperSettings

# Define a function to get organization settings lazily and safely
def get_organization_settings():
    try:
        # Check if settings are configured before accessing the database
        if settings.configured:
            return OrganizationSettings.objects.first()
        # Allow crash if settings are not configured or object not found
    except Exception:
        # Allow crash if any other exception occurs during database access
        raise

ADMIN_EMAIL = SimpleLazyObject(
    lambda: getattr(get_organization_settings(), 'admin_email', None))


def swagger_helper(tags, model):
    def decorators(func):
        descriptions = {
            "list": f"Retrieve a list of {model}",
            "retrieve": f"Retrieve details of a specific {model}",
            "create": f"Create a new {model}",
            "partial_update": f"Update a {model}",
            "destroy": f"Delete a {model}",
        }

        action_type = func.__name__
        get_description = descriptions.get(action_type, f"{action_type} {model}")
        return swagger_auto_schema(manual_parameters=PAGINATION_PARAMS, operation_id=f"{action_type} {model}", operation_description=get_description, tags=[tags])(func)

    return decorators


def initiate_refund(order):
    try:
        if order.payment_provider == "paystack":
            payload = {"transaction": order.transaction_id}
            headers = {
                "Authorization": f"Bearer {settings.PAYMENT_PROVIDERS['paystack']['secret_key']}",
                "Content-Type": "application/json"
            }
            response = requests.post(
                "https://api.paystack.co/refund",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            notify_admin_for_refund_initiated(order)
            notify_user_for_refunded_order(order)
            return True
        elif order.payment_provider == "flutterwave":
            if not order.transaction_id:
                return False
            url = f"https://api.flutterwave.com/v3/transactions/{order.transaction_id}/refund"
            headers = {
                "Authorization": f"Bearer {settings.PAYMENT_PROVIDERS['flutterwave']['secret_key']}",
                "Content-Type": "application/json"
            }
            payload = {}
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            notify_admin_for_refund_initiated(order)
            notify_user_for_refunded_order(order)
            return True
    except requests.exceptions.RequestException:
        return False


def notify_admin_for_refund_initiated(order):
    admin_email = ADMIN_EMAIL
    user_id = order.user.id
    first_name = order.first_name or ''
    last_name = order.last_name or ''
    phone_no = order.phone_number or 'Not provided'

    if not is_celery_healthy():
        send_refund_initiated_email_synchronously(
            order_id=str(order.id),
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            phone_no=phone_no,
            transaction_id=order.transaction_id,
            amount=str(order.total_amount),
            provider=order.payment_provider,
            admin_email=admin_email
        )
    else:
        send_refund_initiated_notification_email.apply_async(
            kwargs={
                'order_id': str(order.id),
                'user_id': user_id,
                'first_name': first_name,
                'last_name': last_name,
                'phone_no': phone_no,
                'transaction_id': order.transaction_id,
                'amount': str(order.total_amount),
                'provider': order.payment_provider,
                'admin_email': admin_email
            }
        )


def notify_user_for_refunded_order(order):
    user_email = order.email or 'unknown@example.com'
    first_name = order.first_name or 'Customer'
    currency = settings.PAYMENT_CURRENCY
    refund_date = timezone.now().date()

    if not is_celery_healthy():
        refund_confirmation_email(
            order_id=str(order.id),
            user_email=user_email,
            first_name=first_name,
            total_amount=str(order.total_amount),
            refund_date=refund_date
        )
    else:
        refund_confirmation_email.apply_async(
            kwargs={
                'order_id': str(order.id),
                'user_email': user_email,
                'first_name': first_name,
                'total_amount': str(order.total_amount),
                'refund_date': refund_date
            }
        )


def notify_user_for_shipped_order(order):
    user_email = order.email or 'unknown@example.com'
    first_name = order.first_name or 'Customer'
    estimated_delivery = order.estimated_delivery

    if not is_celery_healthy():
        send_shipped_email_synchronously(
            order_id=str(order.id),
            user_email=user_email,
            first_name=first_name,
            estimated_delivery=estimated_delivery
        )
    else:
        send_order_shipped_email.apply_async(
            kwargs={
                'order_id': str(order.id),
                'user_email': user_email,
                'first_name': first_name,
                'estimated_delivery': estimated_delivery
            }
        )


def notify_user_for_delivered_order(order):
    user_email = order.email or 'unknown@example.com'
    first_name = order.first_name or 'Customer'
    delivery_date = order.delivery_date

    if not is_celery_healthy():
        send_delivered_email_synchronously(
            order_id=str(order.id),
            user_email=user_email,
            first_name=first_name,
            delivery_date=delivery_date
        )
    else:
        send_order_delivered_email.apply_async(
            kwargs={
                'order_id': str(order.id),
                'user_email': user_email,
                'first_name': first_name,
                'delivery_date': delivery_date
            }
        )
