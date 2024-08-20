from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from dogs.models import Breed, Dog
from dogs.paginations import CustomPagination
from dogs.serializers import BreedSerializer, DogDetailSerializer, DogSerializer
from users.permissions import IsModer, IsOwner


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="все чики пуки"
))
class DogViewSet(ModelViewSet):
    queryset = Dog.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ("breed",)
    ordering_fields = ("date_born",)
    search_fields = ("name",)
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return DogDetailSerializer
        return DogSerializer

    def perform_create(self, serializer):
        dog = serializer.save()
        dog.owner = self.request.user
        dog.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModer | IsOwner,)
        return super().get_permissions()


class BreedCreateAPIView(CreateAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    permission_classes = (
        ~IsModer,
        IsAuthenticated,
    )

    def perform_create(self, serializer):
        breed = serializer.save()
        breed.owner = self.request.user
        breed.save()


class BreedListAPIView(ListAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    pagination_class = CustomPagination


class BreedRetrieveAPIView(RetrieveAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    permission_classes = (
        IsAuthenticated,
        IsModer | IsOwner,
    )


class BreedUpdateAPIView(UpdateAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    permission_classes = (
        IsAuthenticated,
        IsModer | IsOwner,
    )


class BreedDestroyAPIView(DestroyAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    permission_classes = (
        IsAuthenticated,
        IsOwner | ~IsModer,
    )
