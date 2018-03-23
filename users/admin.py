from django.contrib import admin
from users.models import User
from django.contrib.auth.admin import UserAdmin
from users.forms import EmailUserChangeForm, EmailUserCreationForm
from django.utils.translation import ugettext_lazy as _


class EmailUserAdmin(UserAdmin):
	"""EmailUser Admin model."""

	fieldsets = (
				(None, {
					'fields': ('email', 'first_name', 'last_name', 'password')
				}),
				(_('Permissions'), {
					'fields': ('is_active', 'is_staff', 'is_superuser', 'allowed_roles')
				}),
				(_('Important dates'), {
					'fields': ('last_login', 'date_joined')
				}),
			)
	add_fieldsets = ((
		None, {
			'classes': ('wide',),
			'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'allowed_roles')
		}
	),
	)
	# The forms to add and change user instances
	form = EmailUserChangeForm
	add_form = EmailUserCreationForm
	# The fields to be used in displaying the User model.
	# These override the definitions on the base UserAdmin
	# that reference specific fields on auth.User.
	readonly_fields = ('date_joined', )
	list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
	list_filter = ('is_staff', 'is_superuser', 'is_active', 'allowed_roles')
	search_fields = ('email', 'last_name', 'first_name')
	ordering = ('email', )
	filter_horizontal = ('groups', 'user_permissions')

	def get_inline_instances(self, request, obj=None):
		if not obj:
			return list()
		return super(EmailUserAdmin, self).get_inline_instances(request, obj)


admin.site.register(User, EmailUserAdmin)