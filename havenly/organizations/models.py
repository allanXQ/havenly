from django.db import models
from users.models import BaseUser
import uuid
from havenly.common.models import BaseModel

# Create your models here.
class Organizations(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, blank=False, null=False)
    organization_type = models.TextChoices('organization_type', 'AGENCY INDEPENDENT_AGENT')
    currency = models.CharField(max_length=10, default='USD')
    country = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

# Define roles and permissions within an organization. To allow different roles per user in different organizations.
class OrganizationRoles(BaseModel):
    organization = models.ForeignKey(Organizations, on_delete=models.CASCADE)
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    role_name = models.TextChoices('role_name', 'ADMIN AGENT INDEPENDENT_AGENT RENTER BUYER')
    permissions = models.JSONField(default=dict)  # Store permissions as a JSON object

    def __str__(self):
        return f"{self.role_name} - {self.organization.name}"
    
class OrganizationKYC(BaseModel):
    organization = models.OneToOneField(Organizations, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=50)
    document_number = models.CharField(max_length=100)
    document_image = models.ImageField(upload_to='org_kyc_docs/') # to be migrated to a cloud storage later
    verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"KYC for {self.organization.name} - Verified: {self.verified}"