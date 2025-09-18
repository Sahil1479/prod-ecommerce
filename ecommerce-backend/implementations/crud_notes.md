# Notes on CRUD Operations in Django REST Framework

## 1. APIView Usage

- `APIView` is a class-based view provided by DRF for building custom API endpoints.
- You override HTTP method handlers (`get`, `post`, `put`, `patch`, `delete`) to implement CRUD logic.
- Example:

  ```python
  from rest_framework.views import APIView
  from rest_framework.response import Response
  from rest_framework import status

  class ProductDetailView(APIView):
      def get(self, request, pk):
          # Retrieve logic
          ...
      def put(self, request, pk):
          # Update logic
          ...
      def delete(self, request, pk):
          # Delete logic
          ...
  ```

## 2. Permissions

- Use `permission_classes` to restrict access (e.g., `IsAuthenticated`, `IsAdminUser`).
- Example:

  ```python
  from rest_framework.permissions import IsAuthenticated

  class ProductListView(APIView):
      permission_classes = [IsAuthenticated]
      ...
  ```

- You can create custom permissions by subclassing `BasePermission`.

## 3. Serializers

- Use serializers to validate and transform data between models and JSON.
- Example:

  ```python
  from rest_framework import serializers
  from .models import Product

  class ProductSerializer(serializers.ModelSerializer):
      class Meta:
          model = Product
          fields = '__all__'
  ```

## 4. Other Useful Features

- **Pagination:** Add pagination to list endpoints for large datasets.
- **Filtering:** Use `django-filter` or custom logic for filtering results.
- **Ordering:** Allow ordering via query params (e.g., `?ordering=name`).
- **Throttling:** Limit request rates for users or endpoints.
- **Versioning:** Organize API code by version (see API versioning notes).
- **Authentication:** Use JWT, session, or token authentication.
- **Validation:** Add custom validation in serializers or views.
- **Error Handling:** Return appropriate status codes and error messages.

## 5. Alternatives to APIView

- **Generic Views:** DRF provides generic views (`ListCreateAPIView`, `RetrieveUpdateDestroyAPIView`) for common CRUD patterns.
- **ViewSets:** Use `ModelViewSet` for full CRUD with less boilerplate; register with a router in `urls.py`.

## 6. Example CRUD Endpoints

- **List & Create:**
  ```python
  class ProductListView(APIView):
      def get(self, request):
          # List logic
          ...
      def post(self, request):
          # Create logic
          ...
  ```
- **Retrieve, Update, Delete:**
  ```python
  class ProductDetailView(APIView):
      def get(self, request, pk):
          ...
      def put(self, request, pk):
          ...
      def delete(self, request, pk):
          ...
  ```

## 7. Summary

- Use `APIView` for custom logic, generic views/viewsets for rapid CRUD.
- Always use serializers for data validation.
- Apply permissions, authentication, and other DRF features as needed.
