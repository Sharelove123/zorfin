from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow administrators to edit or delete it.
    Assumes the model instance has an `user` attribute.
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        # Write permissions are only allowed to the admin.
        return bool(request.user and request.user.role == 'admin')
