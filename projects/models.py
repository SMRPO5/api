from django.db import models
from dev_groups.models import DevGroup
from django.conf import settings


class BaseModel(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	modified_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


class Project(BaseModel):
	name = models.CharField(max_length=256)
	buyer_name = models.CharField(max_length=512)
	start_date = models.DateTimeField()
	end_date = models.DateTimeField(null=True, blank=True)
	estimated_end_date = models.DateTimeField()
	dev_group = models.ForeignKey(DevGroup, on_delete=models.CASCADE)
	is_active = models.BooleanField(default=True)


class Comment(BaseModel):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	message = models.TextField()


class CardType(BaseModel):
	name = models.CharField(max_length=256)
	is_active = models.BooleanField(default=True)
	color = models.CharField(max_length=128)


class Lane(BaseModel):
	name = models.CharField(max_length=256)
	order = models.CharField(max_length=512)
	is_active = models.BooleanField(default=True)
	project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='lanes')
	column = models.ManyToManyField('Column', blank=True, related_name='lanes')


class Column(BaseModel):
	name = models.CharField(max_length=256)
	parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subcolumns')
	card_limit = models.PositiveIntegerField()


class LoggedTime(BaseModel):
	task = models.ForeignKey('Task', on_delete=models.CASCADE)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	time = models.PositiveIntegerField()


class Task(BaseModel):
	name = models.CharField(max_length=256)
	card = models.ForeignKey('Card', on_delete=models.CASCADE)
	description = models.TextField()
	assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	is_active = models.BooleanField(default=True)
	comments = models.ManyToManyField(Comment, blank=True)


class Card(BaseModel):
	# BACKLOG = 'backlog'
	# PRODUCT_BACKLOG = 'product_backlog'
	# NEXT = 'next'
	# ANALYSIS_AND_DESIGN = 'analysis_and_design'
	# CODING = 'coding'
	# TESTING = 'testing'
	# INTEGRATION = 'integration'
	# DOCUMENTATION = 'documentation'
	# ACCEPTANCE = 'acceptance'
	# DONE = 'done'
	# ARCHIVE = 'archive'
	# TYPE_CHOICES = (
	# 	(BACKLOG, 'Backlog'),
	# 	(PRODUCT_BACKLOG, 'Product backlog'),
	# 	(NEXT, 'Next'),
	# 	(ANALYSIS_AND_DESIGN, 'Analysis & Design'),
	# 	(CODING, 'Coding'),
	# 	(TESTING, 'Testing'),
	# 	(INTEGRATION, 'Integration'),
	# 	(ACCEPTANCE, 'Acceptance'),
	# 	(DONE, 'Done'),
	# 	(ARCHIVE, 'Archive'),
	# )
	# type = models.CharField(choices=TYPE_CHOICES, max_length=128)
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
	name = models.CharField(max_length=512)
	description = models.TextField()
	assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	priority = models.PositiveIntegerField(choices=priority_choices)
	size = models.PositiveIntegerField()
	deadline = models.DateTimeField()
	lane = models.ForeignKey(Lane, on_delete=models.CASCADE, related_name='cards')
	column = models.ForeignKey(Column, on_delete=models.CASCADE)
	comments = models.ManyToManyField(Comment, related_name='cards', blank=True)



