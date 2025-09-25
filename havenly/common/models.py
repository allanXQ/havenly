from django.db import models

# Create your models here.
class Contact(models.Model):
    organization = models.ForeignKey('organizations.Organization', null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', null=True, blank=True, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(organization__isnull=False) ^ models.Q(user__isnull=False),
                name='contact_has_exactly_one_owner'
            )
        ]

class ContactPhone(models.Model):
    contact = models.ForeignKey(Contact, related_name='phones', on_delete=models.CASCADE)
    number = models.CharField(max_length=20)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ContactEmail(models.Model):
    contact = models.ForeignKey(Contact, related_name='emails', on_delete=models.CASCADE)
    email = models.EmailField()
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Address(models.Model):
    contact = models.ForeignKey(Contact, related_name='addresses', on_delete=models.CASCADE)
    line1 = models.CharField(max_length=255)
    line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
