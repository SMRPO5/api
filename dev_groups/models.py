from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.utils import timezone
from django.db.models.signals import m2m_changed


class DevGroup(models.Model):
    name = models.CharField(max_length=256)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Membership')

    def __str__(self):
        return self.name


# @receiver(m2m_changed, sender='dev_groups.Membership')
# def on_members_change(sender, signal, action, instance, **kwargs):
#     kwargs['qwe'] = 'qwe'
#     for membership in instance.membership_set.all():
#         membership.is_active = False
#         membership.save()


class Membership(models.Model):
    role = models.ManyToManyField(Group)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dev_group = models.ForeignKey(DevGroup, on_delete=models.CASCADE)
    date_joined = models.DateTimeField()
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

