from django.contrib import admin
from django.contrib.auth.models import Group

from .models import DevGroup, Membership

class RoleInline(admin.TabularInline):
	model = Group


class MembershipInline(admin.TabularInline):
	model = Membership
	extra = 2
	inlines = (RoleInline, )


class DevGroupAdmin(admin.ModelAdmin):
	inlines = (MembershipInline, )


admin.site.register(DevGroup, DevGroupAdmin)
