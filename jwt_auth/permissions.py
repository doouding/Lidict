"""
Custom permissions
"""
from rest_framework import permissions

# Note that the `has_object_permission` will not run when do
# `create` (which is `POST` method) action

# These's no need to consider the unauthenticated request because
# they have been block by authentication scheme except those in
# AUTHENTICATION_EXCLUDE settings

class IsOwner(permissions.BasePermission):
    """
    Check whether the resource's owner is authenticated user
    or creating new resource which require no authentication info
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsUser(permissions.BasePermission):
    """
    This permission is used when a request want to retrieve or update
    a user's info.
    The authenticated user must be exactly the same with the user
    which the request want to do something with.
    """
    def has_object_permission(self, request, view, obj):
        return obj == request.user
