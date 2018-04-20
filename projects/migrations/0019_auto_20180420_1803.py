# Generated by Django 2.0.3 on 2018-04-20 16:03

from django.db import migrations, models
import django.db.models.deletion
from django.utils import timezone


def create_board(apps, schema_editor):
    Column = apps.get_model('projects', 'Column')
    Card = apps.get_model('projects', 'Card')
    Board = apps.get_model('projects', 'Board')
    Project = apps.get_model('projects', 'Project')
    DevGroup = apps.get_model('dev_groups', 'DevGroup')

    board = Board.objects.create(name='initial', order='asdfadf')
    project = Project.objects.create(name='Initial', buyer_name='Initial', codename='Initial',
                                     start_date=timezone.now(), estimated_end_date=timezone.now, board=board, dev_group=DevGroup.objects.filter()[0])
    column = Column.objects.create(name='placeholder', card_limit=15)
    for card in Card.objects.all():
        if card.column is None:
            card.column = column
            card.save()


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0018_auto_20180420_1558'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lane',
            name='board',
        ),
        migrations.RemoveField(
            model_name='lane',
            name='columns',
        ),
        migrations.AddField(
            model_name='column',
            name='lane',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE, related_name='columns', to='projects.Lane'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='board',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='projects.Board'),
        ),
    ]
