from rest_framework import serializers
from .models import Organizations, OrganizationRoles, OrganizationKYC


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizations
        fields = '__all__'

class OrganizationRolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationRoles
        fields = '__all__'

class OrganizationKYCSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationKYC
        fields = '__all__'