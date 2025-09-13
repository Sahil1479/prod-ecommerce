from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """Allow only admin/staff users."""
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class IsSeller(permissions.BasePermission):
    """Allow only sellers."""
    def has_permission(self, request, view):
        return request.user and request.user.role == "seller"

class IsCustomer(permissions.BasePermission):
    """Allow only customers."""
    def has_permission(self, request, view):
        return request.user and request.user.role == "customer"