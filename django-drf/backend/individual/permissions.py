from rest_framework.permissions import BasePermission


class IsProfileOwner(BasePermission):
    message = "You are not the owner of this profile"

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return obj.user == request.user
