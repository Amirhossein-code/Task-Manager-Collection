from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
)
from rest_framework import status
from .models import Individual
from .serializers import (
    IndividualSerializer,
    UpdateIndividualSerializer,
    SimpleIndividualSerializer,
)
from .permissions import IsOwner


class IndividualViewSet(ModelViewSet):
    queryset = Individual.objects.all()
    serializer_class = SimpleIndividualSerializer
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action == "me":
            if self.request.method == "PUT":
                return UpdateIndividualSerializer
            if self.request.method == "GET":
                return IndividualSerializer

        return super().get_serializer_class()

    @action(
        detail=False,
        methods=["GET", "PUT"],
        permission_classes=[IsAuthenticated, IsOwner],
    )
    def me(self, request):
        individual = self.get_object()

        if request.method == "GET":
            serializer = IndividualSerializer(individual)
            return Response(serializer.data)
        elif request.method == "PUT":
            serializer = UpdateIndividualSerializer(individual, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    def get_object(self):
        try:
            return Individual.objects.get(user_id=self.request.user.id)
        except Individual.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
