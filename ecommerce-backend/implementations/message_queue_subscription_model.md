
Start the Django App, Redis Server and Celery Worker separately
---

```
Start Celery: python -m celery -A ecommerce worker --pool=solo -l info
Start Redis: redis-server.exe as adminitrator
Start Django: python manage.py runserver
```
## 🔔 Inventory Notification Workflow

### Use Case

1. Customer tries to buy a product → it’s **out of stock**.

   * Customer subscribes for **availability notification**.
2. Seller/Admin updates the product → stock > 0.
3. System triggers a **Celery task** to notify all subscribed customers (via email or notification system).

---

## 🔧 Implementation Steps

### 1. Install dependencies

```bash
pip install celery redis
```

---

### 2. Configure Celery (in `ecommerce-backend/ecommerce_backend/celery.py`)

```python
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_backend.settings')

app = Celery('ecommerce_backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

---

### 3. Add Celery to Django settings (`settings.py`)

```python
# Celery + Redis
CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
```

Also update `__init__.py` inside project:

```python
from __future__ import absolute_import, unicode_literals
from .celery import app as celery_app

__all__ = ('celery_app',)
```

---

### 4. Create Subscription Model (`products/models.py`)

```python
from django.db import models
from django.conf import settings
from .models import Product

class ProductSubscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} subscribed to {self.product.name}"
```

---

### 5. Serializer (`products/serializers.py`)

```python
from rest_framework import serializers
from .models import ProductSubscription

class ProductSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSubscription
        fields = ["id", "user", "product", "subscribed_at"]
```

---

### 6. API View (`products/views.py`)

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Product, ProductSubscription
from .serializers import ProductSubscriptionSerializer
from .tasks import notify_users_product_available

class ProductSubscribeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        product = Product.objects.get(id=product_id)
        subscription, created = ProductSubscription.objects.get_or_create(
            user=request.user, product=product
        )
        if created:
            return Response({"message": "Subscribed for availability notification."}, status=status.HTTP_201_CREATED)
        return Response({"message": "Already subscribed."}, status=status.HTTP_200_OK)
```

---

### 7. Celery Task (`products/tasks.py`)

```python
from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from .models import ProductSubscription, Product

User = get_user_model()

@shared_task
def notify_users_product_available(product_id):
    product = Product.objects.get(id=product_id)
    subscriptions = ProductSubscription.objects.filter(product=product)

    for sub in subscriptions:
        send_mail(
            subject=f"{product.name} is now available!",
            message=f"Hi {sub.user.username},\n\nGood news! {product.name} is back in stock.",
            from_email="noreply@ecommerce.com",
            recipient_list=[sub.user.email],
        )
    subscriptions.delete()  # clear after notification
```

---

### 8. Trigger Task When Stock Updates (`products/signals.py`)

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product
from .tasks import notify_users_product_available

@receiver(post_save, sender=Product)
def check_product_stock(sender, instance, **kwargs):
    if instance.stock > 0:
        notify_users_product_available.delay(instance.id)
```

Add in `apps.py` of products inside ProductsConfig:

```python
def ready(self):
    import products.signals
```

---

### 9. URLs (`products/urls.py`)

```python
from django.urls import path
from .views import ProductSubscribeView

urlpatterns = [
    path("<int:product_id>/subscribe/", ProductSubscribeView.as_view(), name="product-subscribe"),
]
```

---

## ✅ Testing the Flow

### 1. Subscribe to Product

* Method: `POST`
* URL: `http://127.0.0.1:8000/api/v1/products/5/subscribe/`
* Auth: Bearer Token

**Response**

```json
{"message": "Subscribed for availability notification."}
```

---

### 2. Seller Updates Stock

* Update product via Admin Panel or API (`PATCH /products/5/`) → `stock: 10`

➡️ Celery task runs → all subscribers get email notification.

---