from rest_framework.permissions import BasePermission


class IsObjectOwner(BasePermission):
    """
    Used for object with individual in their fields
    """

    message = "You need to be the owner of the object to be able to view it"

    def has_object_permission(self, request, view, obj):
        # Check if the request method is safe (GET, HEAD, OPTIONS)
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Ensure that only the user who created the object can delete or update it
            return obj.individual.id == request.user.individual.id

        return False
