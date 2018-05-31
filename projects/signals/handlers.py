from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from fieldsignals import pre_save_changed
import reversion
from django.utils import timezone

from projects.models import Card, Column, Project, Lane, CardType, Board


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
				old_column = Column.objects.get(id=old)
				if reversion.is_active():
					reversion.set_comment('Card moved from %s to %s' % (old_column.name, instance.column.name))

				if old_column.column_type == Column.DONE and instance.column.column_type == Column.REQUESTED:
					card_type, created = CardType.objects.get_or_create(name='Rejected', color='#a80fa8')
					instance.type = card_type


@receiver(pre_save_changed, sender=Project, fields=['board'])
def log_history_on_column_change(sender, instance, changed_fields=None, **kwargs):
	if instance.id:  # Only execute if card actually exists and is not being created
		for field, (old, new) in changed_fields.items():
			if field.name == 'board':
				if old is None or instance.board is None:
					continue
				old_board = Board.objects.get(id=old)

				if old_board.id != instance.board.id:
					for card in instance.cards.all():
						new_column = instance.board.columns.filter(name=card.column.name)[0]
						card.column = new_column
						card.save()


@receiver(post_save, sender=Project)
def create_lane_for_project(sender, instance, **kwargs):
	if kwargs.get('created', False):
		lane, created = Lane.objects.get_or_create(project=instance)
