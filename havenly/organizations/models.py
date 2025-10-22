from django.db import models
from users.models import BaseUser
from havenly.common.models import BaseModel, BaseKYCModel

# Create your models here.
class Organizations(BaseModel):
    OrganizationType = models.TextChoices('organization_type', 'AGENCY INDEPENDENT_AGENT')
    name = models.CharField(max_length=255, blank=False, null=False)
    organization_type = models.CharField(max_length=20, choices=OrganizationType.choices)
    currency = models.CharField(max_length=3, default='USD')
    country = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.name

# Define roles and permissions within an organization. To allow different roles per user in different organizations.
class OrganizationRoles(BaseModel):
    RoleName = models.TextChoices('role_name', 'ADMIN AGENT RENTER BUYER')
    organization = models.ForeignKey(Organizations, on_delete=models.CASCADE)
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    role_name = models.CharField(max_length=6, choices=RoleName.choices)
    permissions = models.JSONField(default=dict)  # Store permissions as a JSON object

    def __str__(self):
        return f"{self.role_name} - {self.organization.name}"
    
class OrganizationKYC(BaseKYCModel):
    organization = models.OneToOneField(Organizations, on_delete=models.CASCADE)

    def __str__(self):
        return f"KYC for {self.organization.name} - Verified: {self.verified}"