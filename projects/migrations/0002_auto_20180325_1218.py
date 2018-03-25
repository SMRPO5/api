# Generated by Django 2.0.3 on 2018-03-25 10:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lane',
            name='is_active',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lane',
            name='project',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='projects.Project'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='card',
            name='comments',
            field=models.ManyToManyField(related_name='cards', to='projects.Comment'),
        ),
        migrations.AlterField(
            model_name='card',
            name='lane',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='projects.Lane'),
        ),
    ]
