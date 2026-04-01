from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'admin')

class IsAnalystOrAdmin(permissions.BasePermission):
    """
    Allows access to analysts and admin users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role in ['analyst', 'admin'])

class IsViewerOrHigher(permissions.BasePermission):
    """
    Allows access to all authenticated roles (viewer, analyst, admin).
    This is effectively identical to IsAuthenticated, but can be customized later.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
