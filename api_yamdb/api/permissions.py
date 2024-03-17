from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Разрешает доступ только администраторам."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_admin
                                                  or request.user.is_staff)


class IsAdminOrReadOnly(permissions.BasePermission):
    """Разрешает изменять данные только администратору."""

    def has_permission(self, request, view):
        return ((request.method in permissions.SAFE_METHODS)
                or (request.user.is_authenticated
                and request.user.is_admin))


class IsAuthorModeratorAdminOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """Разрешает изменения только авторам, модераторам и администраторам."""

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_admin or request.user.is_moderator)
                or obj.author == request.user)
