# Generated by Django 2.0.3 on 2018-04-18 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0015_auto_20180418_1928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lane',
            name='columns',
            field=models.ManyToManyField(blank=True, related_name='lanes', to='projects.Column'),
        ),
    ]
