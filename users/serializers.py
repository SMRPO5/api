from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from dev_groups.models import Group


class GroupSerializer(serializers.ModelSerializer):

	class Meta:
		model = Group
		fields = ('id', 'name')


class UserSerializer(serializers.ModelSerializer):
	allowed_roles = GroupSerializer(many=True)

	class Meta:
		model = get_user_model()
		exclude = ('password', 'user_permissions')
		read_only_field = ('allowed_roles', )
