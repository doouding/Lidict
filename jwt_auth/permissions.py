from rest_framework import permissions

class IsOwnerOrCreate(permissions.BasePermission):
    """
    Check whether the resource's owner is authenticated user
    or creating new resource which require no authentication info
    """
    def has_object_permission(self, request, view, obj):
        if request.method == 'POST':
            return True
        else:
            return obj.owner == request.user
