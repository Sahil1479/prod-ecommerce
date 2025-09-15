from celery import shared_task
from django.core.mail import send_mail
from .models import Product, ProductSubscription

@shared_task
def notify_users_product_available(product_id):
    print("Task started 1: notify_users_product_available")
    product = Product.objects.get(id=product_id)
    subscriptions = ProductSubscription.objects.filter(product=product)

    for subscription in subscriptions:
        send_mail(
            subject=f"Product Available: {product.name}",
            message=f"The product '{product.name}' is now back in stock. Visit our store to make a purchase!",
            from_email="sahilharpal",
            recipient_list=[subscription.user.email],
            fail_silently=False,
        )
    subscriptions.delete()  # Clear subscriptions after notification
