from rest_framework.permissions import (BasePermission,
                                        IsAuthenticatedOrReadOnly)


class IsAdmin(BasePermission):
    """Разрешено только админу."""
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_admin:
            return True


class AuthorAdminOrReadOnly(IsAuthenticatedOrReadOnly):
    """Авторизованным лицам доступно чтение, автору или админу - всё."""
    def has_object_permission(self, request, view, obj):
        return (
            request.method in 'GET'
            or request.user.is_admin
            or request.user == obj.author
        )


class AdminOrReadOnly(BasePermission):
    """Любому пользователю доступно чтение, админу - всё."""
    def has_permission(self, request, view):
        return (
            request.method in 'GET'
            or request.user.is_authenticated
            and request.user.is_admin
        )
