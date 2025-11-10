import django_filters
from .models import Organizations, OrganizationRoles, OrganizationKYC

class OrganizationFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    organization_type = django_filters.ChoiceFilter(choices=Organizations.OrganizationType.choices)
    country = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Organizations
        fields = ['name', 'organization_type', 'country']

class OrganizationRolesFilter(django_filters.FilterSet):
    role_name = django_filters.ChoiceFilter(choices=OrganizationRoles.name)

    class Meta:
        model = OrganizationRoles
        fields = ['role_name']

class OrganizationKYCFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=OrganizationKYC.Status.choices)

    class Meta:
        model = OrganizationKYC
        fields = ['status']