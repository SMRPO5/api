from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from fieldsignals import pre_save_changed
import reversion
from django.utils import timezone

from projects.models import Card, Column, Project, Lane


@receiver(post_save, sender=Card)
def set_initial_column_on_card(sender, instance, **kwargs):
	if kwargs.get('created', False):
		first_column = Column.objects.filter(board__projects__in=[instance.project], column_type=Column.REQUESTED).order_by('order').first()
		try:
			instance.order = first_column.cards.latest('order').order + 1
		except (Card.DoesNotExist, TypeError) as e:
			instance.order = 1
		reversion.set_comment('Card created')
		instance.save()


@receiver(pre_save_changed, sender=Card, fields=['column'])
def log_history_on_column_change(sender, instance, changed_fields=None, **kwargs):
	if instance.id:  # Only execute if card actually exists and is not being created
		for field, (old, new) in changed_fields.items():
			if field.name == 'column':
				reversion.set_comment('Card moved from %s to %s' % (Column.objects.get(id=old).name, instance.column.name))


@receiver(post_save, sender=Project)
def create_lane_for_project(sender, instance, **kwargs):
	if kwargs.get('created', False):
		lane, created = Lane.objects.get_or_create(project=instance)
