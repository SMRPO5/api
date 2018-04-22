from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from projects.models import Card, Column, Project, Lane


@receiver(post_save, sender=Card)
def set_initial_column_on_card(sender, instance, **kwargs):
	if kwargs.get('created', False):
		first_column = Column.objects.filter(board__projects__in=[instance.project], column_type=Column.REQUESTED).order_by('order').first()
		instance.column = first_column
		try:
			instance.order = first_column.cards.latest('order').order + 1
		except (Card.DoesNotExist, TypeError) as e:
			instance.order = 1
		instance.save()


@receiver(post_save, sender=Project)
def create_lane_for_project(sender, instance, **kwargs):
	if kwargs.get('created', False):
		lane, created = Lane.objects.get_or_create(project=instance)
