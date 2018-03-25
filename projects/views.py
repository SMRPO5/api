from django.contrib.auth import get_user_model
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, \
	DestroyModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.permissions import DjangoModelPermissions


class ProjectViewSet(ModelViewSet):
	serializer_class = ProjectSerializer

	def get_queryset(self):
		return Project.objects.all()


class CommentViewSet(ModelViewSet):
	serializer_class = CommentSerializer

	def get_queryset(self):
		return Comment.objects.all()


class CardTypeViewSet(ModelViewSet):
	serializer_class = CardTypeSerializer

	def get_queryset(self):
		return CardType.objects.all()


class LaneViewSet(ModelViewSet):
	serializer_class = LaneSerializer

	def get_queryset(self):
		return Lane.objects.all()


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

	def get_queryset(self):
		return Card.objects.all()