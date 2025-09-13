from celery import shared_task
import time
from django.core.mail import send_mail

@shared_task
def send_order_confirmation_email(user_email, order_id):
    time.sleep(5)  # simulate processing delay
    send_mail(
        subject="Your Order Confirmation",
        message=f"Your order #{order_id} has been confirmed.",
        from_email="no-reply@ecommerce.com",
        recipient_list=[user_email],
        fail_silently=True,
    )
    return f"Email sent to {user_email} for order {order_id}"
