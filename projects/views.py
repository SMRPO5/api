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


class CardTypeViewSet(ModelViewSet):
	serializer_class = CardTypeSerializer

	def get_queryset(self):
		return CardType.objects.all()


class BoardViewSet(ModelViewSet):
	serializer_class = BoardSerializer

	def get_queryset(self):
		if self.request.user.is_kanban_master_allowed() or self.request.user.is_superuser:
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
	# filter_fields = ('object_id', )

	def get_queryset(self):
		# return Version.objects.get_for_object(Card.objects.get(id=self.kwargs['card_id']))
		return Version.objects.get_for_model(Card)
