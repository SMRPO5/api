# Generated by Django 2.0.3 on 2018-04-20 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0016_auto_20180418_1929'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='codename',
            field=models.CharField(default='kjdfhgk', max_length=512),
            preserve_default=False,
        ),
    ]