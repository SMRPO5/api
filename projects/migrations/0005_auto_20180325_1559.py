# Generated by Django 2.0.3 on 2018-03-25 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20180325_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='comments',
            field=models.ManyToManyField(null=True, related_name='cards', to='projects.Comment'),
        ),
    ]
