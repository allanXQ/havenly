from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from havenly.common.models import BaseModel

# Create your models here.
class BaseUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True) # to be migrated to a cloud storage later
    language_preference = models.CharField(max_length=10, default='en')
    theme_preference = models.CharField(max_length=10, default='light')

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.user_type}"

class UserKYC(BaseModel):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=50)
    document_number = models.CharField(max_length=100)
    document_image = models.ImageField(upload_to='kyc_docs/') # to be migrated to a cloud storage later
    verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"KYC for {self.user.username} - Verified: {self.verified}"