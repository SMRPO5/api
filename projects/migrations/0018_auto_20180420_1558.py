# Generated by Django 2.0.3 on 2018-04-20 13:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0017_auto_20180419_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='lane',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='projects.Lane'),
        ),
    ]