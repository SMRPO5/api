from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group
from django.utils import timezone


class DevGroup(models.Model):
    name = models.CharField(max_length=256)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Membership')

    def __str__(self):
        return self.name


class Membership(models.Model):
    role = models.ManyToManyField(Group)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dev_group = models.ForeignKey(DevGroup, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    date_removed = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.is_active:
            self.date_joined = timezone.now()
            self.date_removed = None
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.date_removed = timezone.now()
        self.save()

