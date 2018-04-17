from django.contrib import admin
from .models import *


admin.site.register(Project)
admin.site.register(CardType)
admin.site.register(Card)
admin.site.register(Lane)
admin.site.register(Column)
admin.site.register(Comment)
admin.site.register(LoggedTime)
admin.site.register(Task)

# Register your models here.
