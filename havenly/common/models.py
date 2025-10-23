from django.db import models
import uuid

# Create your models here.
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

# Separate kyc models to allow for independent extension in future
class BaseKYCModel(BaseModel):
    Status = models.TextChoices('status', 'PENDING VERIFIED REJECTED')
    document_type = models.CharField(max_length=50)
    document_number = models.CharField(max_length=100)
    document_image = models.ImageField(upload_to='kyc_docs/') # to be migrated to a cloud storage later
    status = models.CharField(max_length=9, choices=Status.choices, default=Status.PENDING)
    rejection_reason = models.CharField(max_length=200, null=True, blank=True)
    class Meta:
        abstract = True

# Im using this approach because contacts can belong to either organizations or users.
# Each contact can have multiple phone numbers, emails, and addresses associated with it.
class Contact(BaseModel):
    organization = models.ForeignKey('organizations.Organizations', null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey('users.BaseUserModel', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(organization__isnull=False) ^ models.Q(user__isnull=False),
                name='contact_has_exactly_one_owner'
            )
        ]

class ContactPhone(BaseModel):
    contact = models.ForeignKey(Contact, related_name='phones', on_delete=models.CASCADE)
    number = models.CharField(max_length=20)
    is_primary = models.BooleanField(default=False)

class ContactEmail(BaseModel):
    contact = models.ForeignKey(Contact, related_name='emails', on_delete=models.CASCADE)
    email = models.EmailField()
    is_primary = models.BooleanField(default=False)

class Address(BaseModel):
    contact = models.ForeignKey(Contact, related_name='addresses', on_delete=models.CASCADE)
    line1 = models.CharField(max_length=255)
    line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    is_primary = models.BooleanField(default=False)
