import json

from rest_framework import serializers
from reversion.models import Version, Revision

from dev_groups.models import DevGroup
from dev_groups.serializers import DevGroupSerializer
from .models import Project, Comment, CardType, Lane, LoggedTime, Task, Card, Column, Board, WIPViolation
from users.serializers import UserSerializer
from django.contrib.auth import get_user_model
import dateutil.parser


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
	assignee = UserSerializer(fields=('id', 'email', 'first_name', 'last_name'), read_only=True, required=False)
	tasks = TaskSerializer(many=True, read_only=True)
	is_in_requested = serializers.ReadOnlyField()
	is_in_done = serializers.ReadOnlyField()
	is_in_progress = serializers.ReadOnlyField()
	is_in_silver_bullet = serializers.ReadOnlyField()
	is_in_acceptance = serializers.ReadOnlyField()

	def to_internal_value(self, data):
		self.fields['assignee'] = serializers.PrimaryKeyRelatedField(write_only=True, required=False, allow_null=True, queryset=get_user_model().objects.all())
		self.fields['type'] = serializers.PrimaryKeyRelatedField(write_only=True, required=True, queryset=CardType.objects.all())
		return super().to_internal_value(data)

	def to_representation(self, card):
		self.fields['assignee'] = UserSerializer(read_only=True, fields=('id', 'email', 'first_name', 'last_name'))
		self.fields['type'] = CardTypeSerializer(read_only=True)
		return super(CardSerializer, self).to_representation(card)

	class Meta:
		model = Card
		fields = '__all__'
		extra_kwargs = {
			'column': {
				'required': False
			}
		}


class ChildColumnSerializer(serializers.ModelSerializer):
	subcolumns = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
	has_cards = serializers.ReadOnlyField()
	cards = CardSerializer(many=True, read_only=True)

	class Meta:
		model = Column
		fields = '__all__'


class ColumnSerializer(serializers.ModelSerializer):
	subcolumns = ChildColumnSerializer(many=True, required=False)
	has_cards = serializers.ReadOnlyField()
	card_count = serializers.ReadOnlyField()
	cards = CardSerializer(many=True, read_only=True)

	class Meta:
		model = Column
		fields = '__all__'
		extra_kwargs = {
			'first_boundary_column': {
				'required': True
			},
			'second_boundary_column': {
				'required': True
			},
			'high_priority_column': {
				'required': True
			},
			'acceptance_ready_column': {
				'required': True
			}
		}


class BoardUpdateSerializer(serializers.Serializer):
	board = serializers.PrimaryKeyRelatedField(queryset=Board.objects.all())
	board_name = serializers.CharField()
	columns = ColumnSerializer(many=True)

	def update(self, instance, validated_data):
		pass

	def create(self, validated_data):
		board = validated_data.pop('board')
		name = self.initial_data.pop('board_name')
		columns = self.initial_data.pop('columns')
		board.name = name
		board.save()
		order = 0
		suborder = 0
		column_type = Column.REQUESTED
		for col in columns:
			column = Column.objects.get(id=col['id'])
			if column.first_boundary_column:
				column_type = Column.IN_PROGRESS
			if column.second_boundary_column:
				column_type = Column.DONE
			column.column_type = column_type
			column.order = order
			column.subcolumns.clear()
			for subcol in col['subcolumns']:
				subcolumn = Column.objects.get(id=subcol['id'])
				if subcolumn.first_boundary_column:
					column_type = Column.IN_PROGRESS
				if subcolumn.second_boundary_column:
					column_type = Column.DONE
				subcolumn.parent = column
				subcolumn.column_type = column_type
				subcolumn.order = suborder
				subcolumn.save()
				column.column_type = None
				suborder += 1
			column.save()
			order += 1
		return {'board': board, 'board_name': board.name, 'columns': []}


class ProjectSerializer(serializers.ModelSerializer):
	has_cards = serializers.ReadOnlyField()
	# lane = LaneSerializer(read_only=True)
	dev_group = DevGroupSerializer()

	def to_internal_value(self, data):
		self.fields['dev_group'] = serializers.PrimaryKeyRelatedField(write_only=True, required=True, queryset=DevGroup.objects.all())
		return super().to_internal_value(data)

	def to_representation(self, project):
		self.fields['dev_group'] = DevGroupSerializer(read_only=True)
		return super().to_representation(project)

	class Meta:
		model = Project
		fields = '__all__'


class LaneSerializer(serializers.ModelSerializer):
	cards = CardSerializer(source='project.cards', many=True, read_only=True)
	project = ProjectSerializer()

	def to_representation(self, instance):
		return super().to_representation(instance)

	class Meta:
		model = Lane
		fields = '__all__'


class BoardSerializer(serializers.ModelSerializer):
	columns = ColumnSerializer(many=True, read_only=True)
	has_silver_bullet = serializers.ReadOnlyField()
	# lanes = LaneSerializer(source='project.lanes', many=True, read_only=True)
	projects = ProjectSerializer(many=True, read_only=True)

	class Meta:
		model = Board
		fields = '__all__'
		extra_kwargs = {
			'owner': {
				'read_only': True
			}
		}


class WIPViolationSerializer(serializers.ModelSerializer):
	violation_by = UserSerializer(fields=('id', 'email', 'first_name', 'last_name'), read_only=True)
	card = CardSerializer()

	class Meta:
		model = WIPViolation
		fields = '__all__'


class RevisionSerializer(serializers.ModelSerializer):
	user = UserSerializer(fields=('id', 'email', 'first_name', 'last_name'), read_only=True)

	class Meta:
		model = Revision
		fields = '__all__'


class RevisionCardSerializer(serializers.ModelSerializer):
	serialized_data = serializers.JSONField()
	revision = RevisionSerializer()

	def to_representation(self, instance):
		instance.serialized_data = json.loads(instance.serialized_data)
		return super().to_representation(instance)

	class Meta:
		model = Version
		fields = '__all__'


class AnalyticsLeadTimeSerializer(serializers.ModelSerializer):
	#serialized_data = serializers.JSONField()
	#revision = RevisionSerializer()

	def __str__(self):
		return 'qwrwer'

	def to_representation(self, instance):
		creation_date_interval = None
		finished_date_interval = None
		development_date_interval = None
		type = None
		size_interval = None

		project = self.context['request'].data['project']
		start_column = self.context['request'].data['start_column']
		end_column = self.context['request'].data['end_column']
		if 'start_creation_date' in self.context['request'].data:
			creation_date_interval = (
				self.context['request'].data['start_creation_date'],
				self.context['request'].data['end_creation_date']
			)

		if 'start_finished_date' in self.context['request'].data:
			finished_date_interval = (
				self.context['request'].data['start_finished_date'],
				self.context['request'].data['end_finished_date']
			)

		if 'start_development_date' in self.context['request'].data:
			development_date_interval = (
				self.context['request'].data['start_development_date'],
				self.context['request'].data['end_development_date']
			)

		if 'type' in self.context['request'].data:
			type = self.context['request'].data['type']

		if 'from_size' in self.context['request'].data:
			size_interval = (
				self.context['request'].data['from_size'],
				self.context['request'].data['to_size']
			)

		lane = Lane.objects.get(project=project)
		start_column_obj = Column.objects.get(id=start_column)
		end_column_obj = Column.objects.get(id=end_column)
		possibleColumns = Column.objects.filter(board=lane.project.board.id, order__range=(start_column_obj.order, end_column_obj.order)).order_by('order')
		card = json.loads(instance.serialized_data)[0]['fields']
		revision = instance.revision

		is_requested_project = card['project'] == project
		is_card_move = 'Card moved from' in revision.comment
		is_card_in_possible_column = any(column.id == card['column'] for column in possibleColumns)
		is_in_creation_date_interval = True if creation_date_interval is None else dateutil.parser.parse(creation_date_interval[0]) <= dateutil.parser.parse(card['created_at']) <= dateutil.parser.parse(creation_date_interval[1])
		is_in_finished_date_interval = True if finished_date_interval is None or card['end_date'] is None else dateutil.parser.parse(finished_date_interval[0]) <= dateutil.parser.parse(card['end_date']) <= dateutil.parser.parse(finished_date_interval[1])
		is_in_development_date_interval = True if development_date_interval is None or card['development_started'] is None else dateutil.parser.parse(development_date_interval[0]) <= dateutil.parser.parse(card['development_started']) <= dateutil.parser.parse(development_date_interval[1])
		is_correct_type = True if type is None else card['type'] == type
		is_in_size_interval = True if size_interval is None or card['size'] is None else size_interval[0] <= card['size'] <= size_interval[1]

		if not (is_requested_project and is_card_move and is_card_in_possible_column and is_in_creation_date_interval and
					is_in_finished_date_interval and is_in_development_date_interval and is_correct_type and is_in_size_interval):
			return None

		new_instance = {
			'id': instance.object.id,
			'date_created': revision.date_created,
			'column': card['column']
		}

		return new_instance

	class Meta:
		model = Version
		fields = '__all__'

