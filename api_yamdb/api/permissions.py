from rest_framework import permissions


class IsAuthorModeratorAdminOrReadOnly(permissions.BasePermission):
    """
    1.Разрешает доступ к ресурсу если используется безопасный метод, или в
    случае, когда пользователь аутентифицирован.
    2.Разрешает доступ к объекту если используется безопасный
    метод, или пользователь - это автор объекта -
    модератор, админ или суперюзер.
    """

    def has_object_permission(self, request, view, obj):
        return (
                request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_admin
                or request.user.is_moderator
                or request.user.is_superuser
        )

    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
        )
