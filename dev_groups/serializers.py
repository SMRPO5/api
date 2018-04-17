from rest_framework import serializers
from .models import DevGroup, Membership
from django.contrib.auth import get_user_model


class MembershipSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='email', queryset=get_user_model().objects.all())
    dev_group = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Membership
        fields = '__all__'


class DevGroupSerializer(serializers.ModelSerializer):
    members = MembershipSerializer(source='membership_set', many=True)

    def create(self, validated_data):
        memberships = validated_data.get('membership_set')
        dev_group = DevGroup.objects.create(name=validated_data.get('name'))

        for membership in memberships:
            m, created = Membership.objects.get_or_create(user=membership.get('user'), dev_group=dev_group)
            m.role.set(membership.get('role'))

        return dev_group

    def update(self, instance, validated_data):
        for membership in instance.members.all():
            m = Membership.objects.get(user=membership, dev_group=instance)
            if not any(m_validated['user'] == membership for m_validated in validated_data.get('membership_set')):
                m.delete()
            else:
                m = Membership.objects.get(user=membership, dev_group=instance)
                if not m.is_active:
                    m.is_active = True
                    m.save()
        return instance

    class Meta:
        model = DevGroup
        fields = '__all__'
