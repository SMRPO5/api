from rest_framework import serializers
from .models import Project, Comment, CardType, Lane, LoggedTime, Task, Card, Column, Board
from users.serializers import UserSerializer
from django.contrib.auth import get_user_model


class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = '__all__'
		read_only_fields = ('date_created', 'date_changed')


class LoggedTimeSerializer(serializers.ModelSerializer):
	class Meta:
		model = LoggedTime
		fields = '__all__'


class CardTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = CardType
		fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
	class Meta:
		model = Task
		fields = '__all__'


class CardSerializer(serializers.ModelSerializer):
	assignee = UserSerializer(fields=('id', 'email', 'first_name', 'last_name'))
	tasks = TaskSerializer(many=True, read_only=True)

	def to_internal_value(self, data):
		self.fields['assignee'] = serializers.PrimaryKeyRelatedField(write_only=True, required=True, queryset=get_user_model().objects.all())
		self.fields['type'] = serializers.PrimaryKeyRelatedField(write_only=True, required=True, queryset=CardType.objects.all())
		return super().to_internal_value(data)

	def to_representation(self, card):
		self.fields['assignee'] = UserSerializer(read_only=True, fields=('id', 'email', 'first_name', 'last_name'))
		self.fields['type'] = CardTypeSerializer(read_only=True)
		return super(CardSerializer, self).to_representation(card)

	class Meta:
		model = Card
		fields = '__all__'


class ChildColumnSerializer(serializers.ModelSerializer):
	class Meta:
		model = Column
		fields = '__all__'


class ColumnSerializer(serializers.ModelSerializer):
	subcolumns = ChildColumnSerializer(many=True, read_only=True)

	class Meta:
		model = Column
		fields = '__all__'


class LaneSerializer(serializers.ModelSerializer):
	cards = CardSerializer(source='project.cards', many=True, read_only=True)

	def to_representation(self, instance):
		return super().to_representation(instance)

	class Meta:
		model = Lane
		fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
	has_cards = serializers.ReadOnlyField()
	lane = LaneSerializer(read_only=True)

	class Meta:
		model = Project
		fields = '__all__'


class BoardSerializer(serializers.ModelSerializer):
	columns = ColumnSerializer(many=True, read_only=True)
	# lanes = LaneSerializer(source='project.lanes', many=True, read_only=True)
	# projects = ProjectSerializer(many=True, read_only=True)

	class Meta:
		model = Board
		fields = '__all__'