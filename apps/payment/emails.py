import logging
import os
from django.core.mail import send_mail
from django.conf import settings
from django.template import Template, Context
from datetime import datetime

logger = logging.getLogger(__name__)

# Base directory for email templates (relative to this file)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# def send_confirmation_email(order_id, user_email, first_name, total_amount):
#     try:
#         send_order_confirmation_email.delay(order_id, user_email, first_name, total_amount)
#         logger.info("Queued email task via Celery", extra={'order_id': order_id, 'user_email': user_email})
#     except (OperationalError, AttributeError) as e:
#         logger.warning("Celery not configured or failed", extra={'order_id': order_id, 'error': str(e)})
#         subject = f"Order Confirmation - Order #{order_id}"
#         message = (
#             f"Dear {first_name},\n\n"
#             f"Thank you for your order! Your order (#{order_id}) has been successfully placed.\n"
#             f"Total Amount: {settings.PAYMENT_CURRENCY} {total_amount}\n"
#             f"We’ll notify you once your order ships.\n\n"
#             f"Best regards,\nASLUXURY ORIGINALS Team"
#         )
#         try:
#             send_mail(
#                 subject,
#                 message,
#                 settings.EMAIL_HOST_USER,
#                 [user_email],
#                 fail_silently=False,
#             )
#             logger.info("Sent email synchronously", extra={'order_id': order_id, 'user_email': user_email})
#         except Exception as email_err:
#             logger.exception("Failed to send email synchronously",
#                              extra={'order_id': order_id, 'user_email': user_email, 'error': str(email_err)})


def send_order_confirmation_email(order_id, user_email, first_name, total_amount):
    """
    Send an HTML order confirmation email to the user using templates from the emails directory.

    Args:
        order_id (str): The ID of the order.
        user_email (str): The recipient's email address.
        first_name (str): The user's first name.
        total_amount (str): The total amount of the order.
    """
    try:
        # Context for rendering templates
        context = {
            'order_id': order_id,
            'first_name': first_name,
            'total_amount': total_amount,
            'currency': settings.PAYMENT_CURRENCY,
            'site_url': settings.SITE_URL,
            'current_year': datetime.now().year,  # For the footer
        }

        # Load and render HTML template
        html_template_path = os.path.join(BASE_DIR, 'order_confirmation.html')
        with open(html_template_path, 'r') as f:
            html_template = Template(f.read())
        html_message = html_template.render(Context(context))

        # Load and render plain-text template
        txt_template_path = os.path.join(BASE_DIR, 'order_confirmation.txt')
        with open(txt_template_path, 'r') as f:
            txt_template = Template(f.read())
        plain_message = txt_template.render(Context(context))

        # Send the email
        send_mail(
            subject=f"Order Confirmation - Order #{order_id}",
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user_email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info("HTML order confirmation email sent",
                    extra={'order_id': order_id, 'user_email': user_email})
    except Exception as e:
        logger.exception("Failed to send HTML order confirmation email",
                         extra={'order_id': order_id, 'user_email': user_email, 'error': str(e)})
        raise
    