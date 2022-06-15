from rest_framework.permissions import BasePermission

class IsAdminAccount(BasePermission):
    """
    Allows access only to admin users.
    """
    message="You are not admin"

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)
