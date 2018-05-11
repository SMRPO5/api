from django.db import models
from django.utils import timezone

from dev_groups.models import DevGroup
from django.conf import settings


class BaseModel(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	modified_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


class Comment(BaseModel):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
	message = models.TextField()


class LoggedTime(BaseModel):
	task = models.ForeignKey('Task', on_delete=models.CASCADE)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	time = models.PositiveIntegerField()


class CardType(BaseModel):
	name = models.CharField(max_length=256)
	is_active = models.BooleanField(default=True)
	color = models.CharField(max_length=128)

	def __str__(self):
		return self.name


class Board(BaseModel):
	name = models.CharField(max_length=256)
	order = models.PositiveIntegerField(default=1)
	dAttr = models.IntegerField()
	is_active = models.BooleanField(default=True)

	def __str__(self):
		return self.name

	@property
	def has_silver_bullet(self):
		last_requested_column = self.columns.filter(column_type=Column.REQUESTED).order_by('order').last()
		return Card.objects.filter(project__board=self, column=last_requested_column, type__name='Silver bullet').exists()


class Project(BaseModel):
	name = models.CharField(max_length=256)
	buyer_name = models.CharField(max_length=512)
	codename = models.CharField(max_length=512)
	start_date = models.DateTimeField()
	end_date = models.DateTimeField(null=True, blank=True)
	estimated_end_date = models.DateTimeField()
	board = models.ForeignKey(Board, blank=True, null=True, on_delete=models.CASCADE, related_name='projects')
	dev_group = models.ForeignKey(DevGroup, on_delete=models.CASCADE, null=True, blank=True)
	is_active = models.BooleanField(default=True)

	def __str__(self):
		return self.name

	@property
	def has_cards(self):
		return self.cards.exists()

	def delete(self, *args, **kwargs):
		if self.cards.exists():
			self.is_active = False
			self.save()
		else:
			super().delete(*args, **kwargs)


class Lane(BaseModel):
	is_active = models.BooleanField(default=True)
	project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='lane')

	def __str__(self):
		return self.project.name


class Column(BaseModel):
	REQUESTED = 1
	IN_PROGRESS = 2
	DONE = 3
	column_type_choice = (
		(REQUESTED, 'Requested'),
		(IN_PROGRESS, 'In progress'),
		(DONE, 'Done'),
	)
	name = models.CharField(max_length=256)
	parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subcolumns')
	board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='columns')
	column_type = models.PositiveIntegerField(choices=column_type_choice)
	order = models.PositiveIntegerField()
	card_limit = models.PositiveIntegerField()

	def __str__(self):
		return '%s - %s' % (self.name, self.order)


class Task(BaseModel):
	name = models.CharField(max_length=256)
	card = models.ForeignKey('Card', on_delete=models.CASCADE, related_name='tasks')
	description = models.TextField()
	assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	is_active = models.BooleanField(default=True)
	comments = models.ManyToManyField(Comment, blank=True)

	def __str__(self):
		return self.name


class Card(BaseModel):
	LOW = 4
	AVERAGE = 3
	HIGH = 2
	CRITICAL = 1
	priority_choices = (
		(LOW, 'Low'),
		(AVERAGE, 'Average'),
		(HIGH, 'High'),
		(CRITICAL, 'Critical')
	)
	type = models.ForeignKey(CardType, on_delete=models.CASCADE)
	codename = models.CharField(max_length=512, null=True, blank=True)
	name = models.CharField(max_length=512)
	description = models.TextField()
	assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	order = models.PositiveIntegerField(null=True, blank=True)
	priority = models.PositiveIntegerField(choices=priority_choices)
	size = models.PositiveIntegerField(null=True, blank=True)
	deadline = models.DateTimeField()
	end_date = models.DateTimeField(null=True, blank=True)
	development_started = models.DateTimeField(null=True, blank=True)
	column = models.ForeignKey(Column, on_delete=models.CASCADE, related_name='cards')
	project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='cards')
	comments = models.ManyToManyField(Comment, related_name='cards', blank=True)

	@property
	def is_in_requested(self):
		return self.column.column_type == Column.REQUESTED

	@property
	def is_in_progress(self):
		return self.column.column_type == Column.IN_PROGRESS

	@property
	def is_in_done(self):
		return self.column.column_type == Column.DONE

	@property
	def is_in_silver_bullet(self):
		return self.column == Column.objects.filter(board__projects__in=[self.project], column_type=Column.REQUESTED).order_by('order').last()

	@property
	def is_in_acceptance(self):
		return self.column == Column.objects.filter(board__projects__in=[self.project], column_type=Column.DONE).order_by('order').first()

	def save(self, *args, **kwargs):
		try:
			if self.column.column_type == Column.IN_PROGRESS:
				self.development_started = timezone.now()
			elif self.column.column_type == Column.DONE:
				self.end_date = timezone.now()
			elif self.column.column_type == Column.REQUESTED:
				self.development_started = None
		except Column.DoesNotExist:
			if self.type.name == 'Silver bullet':
				last_column_in_requested = Column.objects.filter(board__projects__in=[self.project], column_type=Column.REQUESTED).order_by('order').last()
				self.column = last_column_in_requested
			else:
				first_column = Column.objects.filter(board__projects__in=[self.project], column_type=Column.REQUESTED).order_by('order').first()
				self.column = first_column
		super().save(*args, **kwargs)

	def __str__(self):
		return self.name


class WIPViolation(BaseModel):
	card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='wip_violations')
	violation_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wip_violations')
	reason = models.TextField()
	column = models.ForeignKey(Column, on_delete=models.CASCADE, related_name='wip_violations')

