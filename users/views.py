from django.contrib.auth import get_user_model, authenticate, login, logout
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, \
	DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import DjangoModelPermissions


class UserViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
	serializer_class = UserSerializer
	permission_classes = (IsAuthenticated, DjangoModelPermissions)

	def get_queryset(self):
		return get_user_model().objects.filter()


class MeViewSet(ListModelMixin, GenericViewSet):
	serializer_class = UserSerializer

	def get_queryset(self):
		return get_user_model().objects.filter()

