from rest_framework import serializers
from .models import Project, Comment, CardType, Lane, LoggedTime, Task, Card, Column, Board
from users.serializers import UserSerializer
from django.contrib.auth import get_user_model


<<<<<<< HEAD
class ProjectSerializer(serializers.ModelSerializer):
	has_cards = serializers.ReadOnlyField()

=======
class CommentSerializer(serializers.ModelSerializer):
>>>>>>> Modify database
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


class BoardSerializer(serializers.ModelSerializer):
	class Meta:
		model = Board
		fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
	class Meta:
		model = Project
		fields = '__all__'


class LaneSerializer(serializers.ModelSerializer):
	class Meta:
		model = Lane
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
		return super().to_internal_value(data)

	def to_representation(self, card):
		self.fields['assignee'] = UserSerializer(read_only=True, fields=('id', 'email', 'first_name', 'last_name'))
		return super(CardSerializer, self).to_representation(card)

	class Meta:
		model = Card
		fields = '__all__'


class ChildColumnSerializer(serializers.ModelSerializer):
	cards = CardSerializer(many=True, read_only=True)

	class Meta:
		model = Column
		fields = '__all__'


class ColumnSerializer(serializers.ModelSerializer):
	subcolumns = ChildColumnSerializer(many=True, read_only=True)
	cards = CardSerializer(many=True, read_only=True)

	class Meta:
		model = Column
		fields = '__all__'
