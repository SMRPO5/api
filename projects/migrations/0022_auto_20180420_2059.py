# Generated by Django 2.0.3 on 2018-04-20 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0021_merge_20180420_1829'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='order',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='column',
            name='order',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]