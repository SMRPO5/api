from django.contrib import admin
from .models import *
from reversion.admin import VersionAdmin


@admin.register(Card)
class CardAdmin(VersionAdmin):
	pass
	# exclude = ('column', )


@admin.register(Lane)
class LanesAdmin(VersionAdmin):
	pass


@admin.register(Board)
class BoardAdmin(VersionAdmin):
	pass


admin.site.register(Project)
admin.site.register(CardType)
admin.site.register(Column)
admin.site.register(Comment)
admin.site.register(LoggedTime)
admin.site.register(Task)

# Register your models here.
