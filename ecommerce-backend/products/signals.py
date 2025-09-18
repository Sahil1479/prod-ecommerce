from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Product
from .tasks import notify_users_product_available
from django.contrib.postgres.search import SearchVector

@receiver(pre_save, sender=Product)
def check_previous_stock(sender, instance, **kwargs):
    print("Signal received: pre_save for Product")
    if instance.pk:  # Only for updates, not new products
        try:
            old_instance = Product.objects.get(pk=instance.pk)
            old_stock = old_instance.stock
            new_stock = instance.stock

            if old_stock <= 0 < new_stock:
                # Stock changed from 0 (or below) to available
                notify_users_product_available.delay(instance.id)  # Call the Celery task
                print(f"Stock updated: {old_stock} -> {new_stock}")
        except Product.DoesNotExist:
            pass



@receiver(post_save, sender=Product)
def update_search_vector(sender, instance, **kwargs):
    Product.objects.filter(id=instance.id).update(
        search_vector=(
            SearchVector("name", weight="A") +
            SearchVector("description", weight="B")
        )
    )