# Generated by Django 2.0.3 on 2018-03-22 22:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dev_groups', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='devgroup',
            name='user',
        ),
        migrations.AddField(
            model_name='devgroup',
            name='name',
            field=models.CharField(default='test', max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='membership',
            name='dev_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dev_groups.DevGroup'),
        ),
        migrations.AddField(
            model_name='membership',
            name='role',
            field=models.ManyToManyField(to='auth.Group'),
        ),
        migrations.AddField(
            model_name='membership',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='devgroup',
            name='members',
            field=models.ManyToManyField(through='dev_groups.Membership', to=settings.AUTH_USER_MODEL),
        ),
    ]
