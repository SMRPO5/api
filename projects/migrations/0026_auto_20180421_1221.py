# Generated by Django 2.0.3 on 2018-04-21 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0025_auto_20180421_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='order',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
