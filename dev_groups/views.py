from django.contrib.auth import get_user_model
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, \
	DestroyModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from .serializers import *
from .permissions import KanBanMasterCanCreateUpdateDelete, KANBAN_MASTER
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.permissions import DjangoModelPermissions
from django.db.models import Prefetch


class DevGroupViewSet(ModelViewSet):
	serializer_class = DevGroupSerializer
	permission_classes = (IsAuthenticated, KanBanMasterCanCreateUpdateDelete)

	def get_queryset(self):
		if self.request.user.is_kanban_master_allowed() or self.request.user.is_superuser:
			return DevGroup.objects.filter().prefetch_related(
				Prefetch('membership_set', queryset=Membership.objects.filter(is_active=True)))

		return DevGroup.objects.filter(membership__user=self.request.user).prefetch_related(
			Prefetch('membership_set', queryset=Membership.objects.filter(is_active=True)))


class MemberShipViewSet(DestroyModelMixin, GenericViewSet):
	serializer_class = MembershipSerializer

	def get_queryset(self):
		return Membership.objects.all()
