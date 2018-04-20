from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from dev_groups.models import Group


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
	"""
	A ModelSerializer that takes an additional `fields` argument that
	controls which fields should be displayed.
	"""

	def __init__(self, *args, **kwargs):
		# Don't pass the 'fields' arg up to the superclass
		fields = kwargs.pop('fields', None)

		# Instantiate the superclass normally
		super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

		if fields is not None:
			# Drop any fields that are not specified in the `fields` argument.
			allowed = set(fields)
			existing = set(self.fields)
			for field_name in existing - allowed:
				self.fields.pop(field_name)


class GroupSerializer(serializers.ModelSerializer):

	class Meta:
		model = Group
		fields = ('id', 'name')


class UserSerializer(DynamicFieldsModelSerializer):
	allowed_roles = GroupSerializer(many=True)
	full_name = serializers.ReadOnlyField()

	class Meta:
		model = get_user_model()
		exclude = ('password', 'user_permissions')
		read_only_field = ('allowed_roles', )
