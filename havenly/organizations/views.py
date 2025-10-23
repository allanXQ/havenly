from django.shortcuts import render
from rest_framework import viewsets
from .models import Organizations, OrganizationRoles, OrganizationKYC
from .serializers import OrganizationSerializer, OrganizationRolesSerializer, OrganizationKYCSerializer
from .filters import OrganizationFilter, OrganizationRolesFilter, OrganizationKYCFilter

# Create your views here.
class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organizations.objects.all()
    serializer_class = OrganizationSerializer
    filterset_class = OrganizationFilter

class OrganizationRolesViewSet(viewsets.ModelViewSet):
    queryset = OrganizationRoles.objects.all()
    serializer_class = OrganizationRolesSerializer
    filterset_class = OrganizationRolesFilter

class OrganizationKYCViewSet(viewsets.ModelViewSet):
    queryset = OrganizationKYC.objects.all()
    serializer_class = OrganizationKYCSerializer
    filterset_class = OrganizationKYCFilter 