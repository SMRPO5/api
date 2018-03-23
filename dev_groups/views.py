from django.contrib.auth import get_user_model
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, \
	DestroyModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.permissions import DjangoModelPermissions


class DevGroupViewSet(ModelViewSet):
    serializer_class = DevGroupSerializer
    # permission_classes = [AllowAny]

    def get_queryset(self):
        return DevGroup.objects.all()

