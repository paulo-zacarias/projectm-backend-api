from rest_framework import permissions
from .models import Sprint


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow admin of an project to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.admin == request.user


class IsProjectParticipant(permissions.BasePermission):
    """
    Global permission check for blacklisted IPs.
    """

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            # Check permissions for read-only request
            return True
        else:
            # Check permissions for write request
            username = request.user.username
            is_participant = Sprint.objects.get(id=1).project.participants.filter(username=username).exists()
            return is_participant




