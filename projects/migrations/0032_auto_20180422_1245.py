# Generated by Django 2.0.3 on 2018-04-22 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0031_auto_20180422_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='column',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='projects.Column'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='card',
            name='project',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='projects.Project'),
            preserve_default=False,
        ),
    ]