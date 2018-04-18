from django.contrib import admin
from .models import DevGroup, Membership


class MembershipInline(admin.TabularInline):
	model = Membership
	extra = 2


class DevGroupAdmin(admin.ModelAdmin):
	inlines = (MembershipInline, )


admin.site.register(DevGroup, DevGroupAdmin)
