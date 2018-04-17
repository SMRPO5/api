from django.contrib.auth import get_user_model
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, \
	DestroyModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.permissions import DjangoModelPermissions


class DevGroupViewSet(ModelViewSet):
	serializer_class = DevGroupSerializer

	def get_queryset(self):
		return DevGroup.objects.all()


class MemberShipViewSet(DestroyModelMixin, GenericViewSet):

	serializer_class = MembershipSerializer

	def get_queryset(self):
		return Membership.objects.all()

