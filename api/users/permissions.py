from rest_framework import permissions


class IsAdminOrIsSelf(permissions.BasePermission):
    """
    Object-level permission to only allow admin users or the own user to update it.
    """

    def has_object_permission(self, request, view, obj):

        if request.method == 'PUT' or 'PATCH':
            if request.user.is_staff:
                return True

            return obj.pk == request.user.pk

        return False
