from django.contrib.auth.models import Group
from django.db.models import Prefetch
from rest_framework import serializers
from .models import DevGroup, Membership
from django.contrib.auth import get_user_model
from rest_framework.utils import model_meta


class RoleSerializer(serializers.ModelSerializer):

	class Meta:
		model = Group
		exclude = ('permissions', )


class MembershipSerializer(serializers.ModelSerializer):
	user = serializers.SlugRelatedField(slug_field='email', queryset=get_user_model().objects.all())
	first_name = serializers.SlugRelatedField(source='user', slug_field='first_name', read_only=True)
	last_name = serializers.SlugRelatedField(source='user', slug_field='last_name', read_only=True)
	user_id = serializers.SlugRelatedField(source='user', slug_field='id', read_only=True)
	dev_group = serializers.PrimaryKeyRelatedField(read_only=True)
	role = RoleSerializer(many=True)

	def to_internal_value(self, data):
		self.fields['role'] = serializers.PrimaryKeyRelatedField(many=True, write_only=True, required=True, queryset=Group.objects.all())
		return super().to_internal_value(data)

	def to_representation(self, membership):
		self.fields['role'] = RoleSerializer(read_only=True, many=True)
		return super().to_representation(membership)

	class Meta:
		model = Membership
		fields = '__all__'


class DevGroupSerializer(serializers.ModelSerializer):
	members = MembershipSerializer(source='membership_set', many=True)

	def validate_members(self, value):
		if not (any('Kanban Master' in map(lambda x: x.name, membership['role']) for membership in value) and
				any('Developer' in map(lambda x: x.name, membership['role']) for membership in value) and
				any('Product Owner' in map(lambda x: x.name, membership['role']) for membership in value)):
			raise serializers.ValidationError('All roles must be filled.')
		return value

	def create(self, validated_data):
		memberships = validated_data.get('membership_set')
		dev_group = DevGroup.objects.create(name=validated_data.get('name'))

		for membership in memberships:
			m, created = Membership.objects.get_or_create(user=membership.get('user'), dev_group=dev_group)
			m.role.set(membership.get('role'))

		return dev_group

	def update(self, instance, validated_data):
		membership_set = validated_data.pop('membership_set', [])
		for m in instance.membership_set.all():
			if m.is_active and not any(m.user == a['user'] for a in membership_set):
				m.delete()

		for membership in membership_set:
			roles = membership.pop('role')
			m, created = Membership.objects.get_or_create(**membership, dev_group=instance)

			m.role.set(roles)
			if not m.is_active and any(m.user == a['user'] for a in membership_set):
				m.is_active = True
				m.save()
		instance = super().update(instance, validated_data)
		return DevGroup.objects.filter(id=instance.id).prefetch_related(Prefetch('membership_set', queryset=Membership.objects.filter(is_active=True)))[0]


	class Meta:
		model = DevGroup
		fields = '__all__'
