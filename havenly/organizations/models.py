from django.db import models
from common.models import BaseModel, BaseKYCModel

# Create your models here.
class Organizations(BaseModel):
    OrganizationType = models.TextChoices('organization_type', 'AGENCY INDEPENDENT_AGENT')
    name = models.CharField(max_length=255, blank=False, null=False)
    organization_type = models.CharField(max_length=20, choices=OrganizationType.choices, blank=False, null=False)
    currency = models.CharField(max_length=3, default='USD')
    country = models.CharField(max_length=15, blank=False, null=False)

    def __str__(self):
        return self.name
    
class OrganizationKYC(BaseKYCModel):
    organization = models.OneToOneField(Organizations, on_delete=models.CASCADE)

    def __str__(self):
        return f"KYC for {self.organization.name} - Verified: {self.verified}"

class Permission(BaseModel):
    """
    Granular permission definitions
    Examples: 'view_listing', 'create_listing', 'approve_kyc', 'view_reports'
    """
    codename = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    module = models.CharField(max_length=50)  # e.g., 'listing', 'property', 'user', 'financial'
    
    class Meta:
        db_table = 'permissions'
        ordering = ['module', 'name']
    
    def __str__(self):
        return f"{self.module}.{self.codename}"


class OrganizationRoles(BaseModel):
    """
    Roles that can be assigned within organizations
    Can be system-defined or organization-specific custom roles
    """
    name = models.CharField(max_length=100)
    organization = models.ForeignKey(
        Organizations, 
        on_delete=models.CASCADE,
        null=True, 
        blank=True  # Null = system-wide role, not null = org-specific role
    )
    permissions = models.ManyToManyField(Permission, related_name='role_permissions')
    is_system_role = models.BooleanField(default=False)  # System roles can't be deleted
    description = models.TextField(blank=True)
    
    class Meta:
        db_table = 'roles'
    
    def __str__(self):
        return f"{self.name} ({self.organization or 'System'})"


class OrganizationMembership(BaseModel):
    """
    Links users to organizations with their roles
    A user can have multiple roles in the same/different organization
    """
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('pending', 'Pending'),
        ('suspended', 'Suspended'),
    ]
    
    organization = models.ForeignKey(
        Organizations, 
        on_delete=models.CASCADE,
        related_name='membership_organization'
    )
    user = models.ForeignKey(
        'users.BaseUser', 
        on_delete=models.CASCADE,
        related_name='membership_user'
    )
    roles = models.ManyToManyField(OrganizationRoles, related_name='membership_roles')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    reason_for_status_change = models.TextField(blank=True)
    class Meta:
        db_table = 'organization_memberships'
    
    def __str__(self):
        return f"{self.user.email} in {self.organization.name}"