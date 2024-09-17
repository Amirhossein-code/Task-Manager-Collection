from rest_framework.permissions import BasePermission


class IsObjectOwner(BasePermission):
    # Used for object with individual in their fields
    message = "You need to be the owner of the object to be able to view it"

    def has_object_permission(self, request, view, obj):
        return obj.individual.id == request.user.individual.id
