# Generated by Django 2.0.3 on 2018-04-17 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_auto_20180417_0916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
