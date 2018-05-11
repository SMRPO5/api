from django.contrib.auth import get_user_model
from itertools import islice

from django.db.models import Prefetch
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, \
	DestroyModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from reversion.models import Version

from projects.models import WIPViolation
from .serializers import *
from api.permissions import KANBAN_MASTER, KanBanMasterCanCreateUpdateDelete
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.permissions import DjangoModelPermissions
from django_filters import rest_framework as filters
from rest_framework import filters as rest_filters
from django.db.models import When, Case, F
from reversion.views import RevisionMixin
import reversion


class ProjectViewSet(ModelViewSet):
	serializer_class = ProjectSerializer
	filter_backends = (DjangoFilterBackend,)
	permission_classes = (KanBanMasterCanCreateUpdateDelete, IsAuthenticated)

	filter_fields = {
		'dev_group__membership__user': ['exact', 'in']
	}

	def get_queryset(self):
		return Project.objects.filter(is_active=True).prefetch_related('cards')


class CommentViewSet(ModelViewSet):
	serializer_class = CommentSerializer

	def get_queryset(self):
		return Comment.objects.all()


class CardTypeFilterBackend(rest_filters.BaseFilterBackend):
	"""
	Filter that only allows users to see their card types.
	"""
	def filter_queryset(self, request, queryset, view):
		try:
			dev_group = Project.objects.get(id=request.query_params.get('project', None)).dev_group
		except Project.DoesNotExist:
			return queryset.filter()

		if dev_group.is_kanban_master(request.user) and dev_group.is_product_owner(request.user):
			return CardType.objects.all()
		elif dev_group.is_kanban_master(request.user):
			return CardType.objects.exclude(name='Feature request')
		elif dev_group.is_product_owner(request.user):
			return CardType.objects.exclude(name='Silver bullet')

		return CardType.objects.exclude(name__in=['Feature request', 'Silver bullet'])


class CardTypeViewSet(ModelViewSet):
	serializer_class = CardTypeSerializer
	filter_backends = (DjangoFilterBackend, CardTypeFilterBackend)

	def get_queryset(self):
		return CardType.objects.all()


class BoardViewSet(ModelViewSet):
	serializer_class = BoardSerializer

	def get_queryset(self):
		if self.request.user.is_superuser:
			return Board.objects.filter().prefetch_related(
				Prefetch('columns', queryset=Column.objects.filter(parent__isnull=True).order_by('order').prefetch_related('subcolumns')),
				Prefetch('projects', queryset=Project.objects.filter()),
				'projects__cards').distinct()

		return Board.objects.filter(projects__dev_group__members__in=[self.request.user]).prefetch_related(
			Prefetch('columns', queryset=Column.objects.filter(parent__isnull=True).order_by('order').prefetch_related('subcolumns')),
			Prefetch('projects', queryset=Project.objects.filter(dev_group__members__in=[self.request.user])),
			'projects__cards').distinct()


class LaneViewSet(ModelViewSet):
	serializer_class = LaneSerializer

	filter_fields = ('project', 'project__board')

	def get_queryset(self):
		return Lane.objects.filter(project__dev_group__members__in=[self.request.user]).select_related(
			'project__board').prefetch_related('project__cards__assignee',
											   'project__cards__tasks',
											   'project__cards__type')


class ColumnViewSet(ModelViewSet):
	serializer_class = ColumnSerializer
	filter_fields = {
		'lane__project': ['exact', 'in']
	}

	def get_queryset(self):
		return Column.objects.filter(parent__isnull=True).prefetch_related('subcolumns__cards__tasks', 'cards__tasks')


class LoggedTimeViewSet(ModelViewSet):
	serializer_class = LoggedTimeSerializer

	def get_queryset(self):
		return LoggedTime.objects.all()


class TaskViewSet(ModelViewSet):
	serializer_class = TaskSerializer

	def get_queryset(self):
		return Task.objects.all()


class CardViewSet(RevisionMixin, ModelViewSet):
	serializer_class = CardSerializer

	def get_queryset(self):
		return Card.objects.all()

	def update(self, request, *args, **kwargs):
		return super().update(request, *args, **kwargs)


class WIPViolationViewSet(ModelViewSet):
	serializer_class = WIPViolationSerializer
	filter_fields = ('card', )

	def get_queryset(self):
		return WIPViolation.objects.all()

	def perform_create(self, serializer):
		serializer.save(violation_by=self.request.user)


class CardHistoryFilter(filters.FilterSet):
	card = filters.NumberFilter(name='object_id')

	class Meta:
		model = Version
		fields = ('card', )


class CardHistoryViewSet(ListModelMixin, GenericViewSet):
	serializer_class = RevisionCardSerializer
	filter_class = CardHistoryFilter

	def get_queryset(self):
		return Version.objects.get_for_model(Card)
