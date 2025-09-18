# Notes on Serialization in Django REST Framework

Ah nice 👌 foreign keys are super common in serializers, and DRF handles them for you — but how it saves depends on how you **define the field**.

Let’s break it down with an example.

---

## 🔹 Example Model

```python
# products/models.py
from django.db import models
from users.models import User
from categories.models import Category

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
```

---

## 🔹 Default Serializer (Primary Key RelatedField)

```python
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price", "category", "seller"]
```

### How it works

- By default, `category` and `seller` will be represented as **IDs**.
- If you `POST`:

  ```json
  {
    "name": "iPhone Charger",
    "price": "999.00",
    "category": 2,
    "seller": 5
  }
  ```

- In `.save()` → `create()`, DRF will pass `validated_data = {"name": ..., "price": ..., "category": <Category obj>, "seller": <User obj>}`.
  Notice: the integers (`2`, `5`) are converted into model instances before saving.

---

## 🔹 Nested Serializer (if you want extra details)

```python
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)  # Nested detail
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), write_only=True
    )

    class Meta:
        model = Product
        fields = ["id", "name", "price", "category", "category_id", "seller"]
```

### How it works

- Now, `GET` returns:

  ```json
  {
    "id": 1,
    "name": "iPhone Charger",
    "price": "999.00",
    "category": { "id": 2, "name": "Electronics" },
    "seller": 5
  }
  ```

- But when `POST`ing, you send:

  ```json
  {
    "name": "iPhone Charger",
    "price": "999.00",
    "category_id": 2,
    "seller": 5
  }
  ```

- DRF maps `category_id` → actual `Category` object → stores in DB.

---

## 🔹 Summary

- **Default**: ForeignKey fields accept **IDs** and are converted to model instances in `.save()`.
- **Custom (nested)**: You can expose related objects in responses while still accepting IDs for writes.
- The conversion (id → object) happens in **`to_internal_value()`** during `is_valid()`, so by the time `.save()` is called, `validated_data` already has full objects.

---

Perfect 👍 you’ve defined the serializer so that:

- **`tags`** → is **read-only**, returns tag objects (using `TagSerializer`).
- **`tag_ids`** → is **write-only**, accepts a list of tag IDs for create/update.

This is a classic DRF pattern for ManyToMany fields.

---

## 🔹 Example Model

```python
class Tag(models.Model):
    name = models.CharField(max_length=50)

class Product(models.Model):
    name = models.CharField(max_length=100)
    tags = models.ManyToManyField(Tag, related_name="products")
```

---

## 🔹 Serializer

```python
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class ProductSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)  # for GET
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True, write_only=True
    )  # for POST/PUT

    class Meta:
        model = Product
        fields = ["id", "name", "tags", "tag_ids"]

    def create(self, validated_data):
        tag_ids = validated_data.pop("tag_ids", [])
        product = Product.objects.create(**validated_data)
        product.tags.set(tag_ids)   # ✅ ManyToMany needs set()
        return product

    def update(self, instance, validated_data):
        tag_ids = validated_data.pop("tag_ids", None)
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        if tag_ids is not None:
            instance.tags.set(tag_ids)
        return instance
```

---

## 🔹 Request/Response Formats

### ✅ `POST` (create product with tags)

```json
{
  "name": "iPhone Charger",
  "tag_ids": [1, 2, 3]
}
```

### ✅ Response (`GET` or after create)

```json
{
  "id": 10,
  "name": "iPhone Charger",
  "tags": [
    { "id": 1, "name": "Electronics" },
    { "id": 2, "name": "Mobile" },
    { "id": 3, "name": "Accessories" }
  ]
}
```

---

## 🔹 Summary

- **GET** → returns `tags` as objects.
- **POST/PUT** → you must send `tag_ids` as a list of integers.
- Serializer manually handles `.set(tag_ids)` because ManyToMany can’t be directly assigned during `.create()`.

---

## 1. Basic Usage

- Use `serializers.ModelSerializer` for automatic field mapping from models.
- Example:
  ```python
  class ProductSerializer(serializers.ModelSerializer):
      class Meta:
          model = Product
          fields = '__all__'
  ```

## 2. Handling Different Field Types

- **ForeignKey:** Use nested serializers or `PrimaryKeyRelatedField`.

  ```python
  class CategorySerializer(serializers.ModelSerializer):
      class Meta:
          model = Category
          fields = ['id', 'name']

  class ProductSerializer(serializers.ModelSerializer):
      category = CategorySerializer(read_only=True)
      category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True)
      class Meta:
          model = Product
          fields = ['id', 'name', 'catwhat egory', 'category_id']
  ```

- **ManyToMany:** Use nested serializers or list of IDs.

  ```python
  class TagSerializer(serializers.ModelSerializer):
      class Meta:
          model = Tag
          fields = ['id', 'name']

  class ProductSerializer(serializers.ModelSerializer):
      tags = TagSerializer(many=True, read_only=True)
      tag_ids = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, write_only=True)
      class Meta:
          model = Product
          fields = ['id', 'name', 'tags', 'tag_ids']
  ```

## 3. Read-Only & Write-Only Fields

- Use `read_only=True` for fields that should not be updated (e.g., `id`, `created_at`).
- Use `write_only=True` for fields only needed on input (e.g., passwords).
  ```python
  class UserSerializer(serializers.ModelSerializer):
      password = serializers.CharField(write_only=True)
      class Meta:
          model = User
          fields = ['id', 'username', 'password']
  ```

## 4. Private/Confidential Fields

- Exclude sensitive fields from `fields` or use custom logic in `to_representation`.
- Example:
  ```python
  class UserSerializer(serializers.ModelSerializer):
      class Meta:
          model = User
          exclude = ['secret_token']
  ```

## 5. Custom Validation

- Add `validate_<fieldname>` methods for field-level validation.
- Override `validate` for object-level validation.
  ```python
  class ProductSerializer(serializers.ModelSerializer):
      def validate_price(self, value):
          if value < 0:
              raise serializers.ValidationError("Price must be positive.")
          return value
      def validate(self, data):
          # Custom object-level validation
          return data
  ```

## 6. Post Creation Logic

- Use `create` and `update` methods for custom save logic.
  ```python
  class ProductSerializer(serializers.ModelSerializer):
      def create(self, validated_data):
          # Custom creation logic
          return Product.objects.create(**validated_data)
      def update(self, instance, validated_data):
          # Custom update logic
          return super().update(instance, validated_data)
  ```

## 7. Other Useful Features

- **SerializerMethodField:** For computed fields.
- **HyperlinkedModelSerializer:** For hyperlinking related objects.
- **Extra kwargs:** Add options like `required`, `default`, etc. in `Meta.extra_kwargs`.
- **Partial updates:** Use `partial=True` in views for PATCH requests.

## 8. Summary

- Use nested serializers for related models.
- Control field visibility with `read_only`, `write_only`, and `exclude`.
- Add custom validation and creation logic as needed.
- Always protect confidential data and validate input.

## 9. Steps to Test Serialization Cases

### 1. Basic Serialization

- Create an instance of the model and serialize it:
  ```python
  product = Product.objects.create(name="Test", price=10)
  serializer = ProductSerializer(product)
  print(serializer.data)
  ```

### 2. ForeignKey and ManyToMany Fields

- Create related objects and assign them:
  ```python
  category = Category.objects.create(name="Electronics")
  product = Product.objects.create(name="Phone", category=category)
  tag1 = Tag.objects.create(name="Smart")
  tag2 = Tag.objects.create(name="Mobile")
  product.tags.set([tag1, tag2])
  serializer = ProductSerializer(product)
  print(serializer.data)
  ```

### 3. Read-Only and Write-Only Fields

- Try to update a read-only field (should not change).
- Try to create/update with a write-only field (should be accepted on input, not shown on output).

### 4. Private/Confidential Fields

- Ensure excluded fields do not appear in serialized output:
  ```python
  user = User.objects.create(username="testuser", secret_token="abc123")
  serializer = UserSerializer(user)
  print(serializer.data)  # secret_token should not be present
  ```

### 5. Custom Validation

- Try to create/update with invalid data (e.g., negative price):
  ```python
  serializer = ProductSerializer(data={"name": "Test", "price": -5})
  serializer.is_valid()  # Should be False
  print(serializer.errors)
  ```

### 6. Post Creation Logic

- Create an object using the serializer and check custom logic:
  ```python
  serializer = ProductSerializer(data={"name": "Test", "price": 10})
  if serializer.is_valid():
      product = serializer.save()
  ```

### 7. SerializerMethodField and Computed Fields

- Add a computed field and check its value in output.

### 8. Partial Updates

- Use PATCH requests in your API client or tests to update only some fields.

### 9. Error Handling

- Test with missing required fields, invalid types, etc., and check error messages.

---

**Tip:** Use Django shell (`python manage.py shell`) or DRF test cases to run these tests interactively.
