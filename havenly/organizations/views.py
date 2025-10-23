from django.shortcuts import render
from rest_framework import viewsets
from .models import Organizations, OrganizationRoles, OrganizationKYC
from .serializers import OrganizationSerializer, OrganizationRolesSerializer, OrganizationKYCSerializer

# Create your views here.
class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organizations.objects.all()
    serializer_class = OrganizationSerializer

class OrganizationRolesViewSet(viewsets.ModelViewSet):
    queryset = OrganizationRoles.objects.all()
    serializer_class = OrganizationRolesSerializer

class OrganizationKYCViewSet(viewsets.ModelViewSet):
    queryset = OrganizationKYC.objects.all()
    serializer_class = OrganizationKYCSerializer