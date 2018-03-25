from django.db import models
from dev_groups.models import DevGroup
from django.conf import settings


class Project(models.Model):
	name = models.CharField(max_length=256)
	buyer_name = models.CharField(max_length=512)
	project_created_at = models.DateTimeField(auto_now_add=True)
	start_date = models.DateTimeField()
	end_date = models.DateTimeField()
	estimated_end_date = models.DateTimeField()
	dev_group = models.ForeignKey(DevGroup, on_delete=models.CASCADE)
	is_active = models.BooleanField()


class Comment(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	date_created = models.DateTimeField(auto_now_add=True)
	date_changed = models.DateTimeField(auto_now=True)
	message = models.TextField()


class CardType(models.Model):
	name = models.CharField(max_length=256)
	is_active = models.BooleanField()
	color = models.CharField(max_length=128)


class Lane(models.Model):
	name = models.CharField(max_length=256)
	order = models.CharField(max_length=512)
	is_active = models.BooleanField


class LoggedTime(models.Model):
	task = models.ForeignKey('Task', on_delete=models.CASCADE)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	time = models.PositiveIntegerField()


class Task(models.Model):
	name = models.CharField(max_length=256)
	card = models.ForeignKey('Card', on_delete=models.CASCADE)
	description = models.TextField()
	assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	is_active = models.BooleanField()
	comments = models.ManyToManyField(Comment)


class Card(models.Model):
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
	lane = models.ForeignKey(Lane, on_delete=models.CASCADE)
	comments = models.ManyToManyField(Comment)



