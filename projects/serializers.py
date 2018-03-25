from rest_framework import serializers
from .models import Project, Comment, CardType, Lane, LoggedTime, Task, Card


class ProjectSerializer(serializers.ModelSerializer):

	class Meta:
		model = Project
		fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

	class Meta:
		model = Comment
		fields = '__all__'
		read_only_fields = ('date_created', 'date_changed')


class CardTypeSerializer(serializers.ModelSerializer):

	class Meta:
		model = CardType
		fields = '__all__'


class LaneSerializer(serializers.ModelSerializer):

	class Meta:
		model = Lane
		fields = '__all__'


class LoggedTimeSerializer(serializers.ModelSerializer):

	class Meta:
		model = LoggedTime
		fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):

	class Meta:
		model = Task
		fields = '__all__'


class CardSerializer(serializers.ModelSerializer):

	class Meta:
		model = Card
		fields = '__all__'