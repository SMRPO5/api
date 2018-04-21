from django.db import models
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
	order = models.CharField(max_length=512)
	is_active = models.BooleanField(default=True)

	def __str__(self):
		return self.name


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
	name = models.CharField(max_length=256)
	order = models.CharField(max_length=512)
	is_active = models.BooleanField(default=True)
	project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='lane')

	def __str__(self):
		return self.name


class Column(BaseModel):
	name = models.CharField(max_length=256)
	parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subcolumns')
	board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='columns')
	order = models.PositiveIntegerField()
	card_limit = models.PositiveIntegerField()

	def __str__(self):
		return self.name


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
	size = models.PositiveIntegerField()
	deadline = models.DateTimeField()
	column = models.ForeignKey(Column, on_delete=models.CASCADE, related_name='cards', null=True, blank=True)
	project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='cards', null=True, blank=True)
	comments = models.ManyToManyField(Comment, related_name='cards', blank=True)

	def __str__(self):
		return self.name


