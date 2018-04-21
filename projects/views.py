from django.contrib.auth import get_user_model
from itertools import islice
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, \
	DestroyModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from .serializers import *
from api.permissions import KANBAN_MASTER, KanBanMasterCanCreateUpdateDelete
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.permissions import DjangoModelPermissions


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
		return Board.objects.all()


class LaneViewSet(ModelViewSet):
	serializer_class = LaneSerializer

	filter_fields = {
		'project': ['exact']
	}

	def get_queryset(self):
		return Lane.objects.all().select_related('project__board').prefetch_related('project__cards__assignee',
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


class CardViewSet(ModelViewSet):
	serializer_class = CardSerializer

	filter_fields = {
		'lane__project': ['exact', 'in']
	}

	def get_queryset(self):
		return Card.objects.all()
