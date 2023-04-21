from rest_framework.permissions import BasePermission


class IsActive(BasePermission):
    def has_permission(self, request, view):
        return True if request.user.is_active else False
