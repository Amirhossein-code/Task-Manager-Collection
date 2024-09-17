from rest_framework.permissions import BasePermission


class IsProfileOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return obj.user == request.user
