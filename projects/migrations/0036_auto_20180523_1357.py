# Generated by Django 2.0.3 on 2018-05-23 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0035_auto_20180515_1137'),
    ]

    operations = [
        migrations.AddField(
            model_name='column',
            name='acceptance_ready_column',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='column',
            name='first_boundary_column',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='column',
            name='high_priority_column',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='column',
            name='second_boundary_column',
            field=models.BooleanField(default=False),
        ),
    ]
