from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group


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

    def delete(self, *args, **kwargs):
        # TODO auditlog
        self.is_active = False
        self.save()

