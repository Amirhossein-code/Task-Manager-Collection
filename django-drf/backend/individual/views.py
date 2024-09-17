from rest_framework import mixins
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.viewsets import GenericViewSet

from .models import Individual
from .permissions import IsProfileOwner
from .serializers import (
    IndividualSerializer,
    UpdateIndividualSerializer,
)

# Delete and Created methods have been blocked.
# Creation of the individual is handled by the system


class IndividualViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    serializer_class = IndividualSerializer
    permission_classes = [IsAuthenticated, IsProfileOwner]

    def get_serializer_class(self):
        if self.request.method == "PUT":
            return UpdateIndividualSerializer

        return IndividualSerializer

    def get_queryset(self):
        return Individual.objects.filter(user_id=self.request.user.id).all()
