from django.db import models
from django.contrib.auth.models import AbstractUser
from common.models import BaseKYCModel


# Create your models here.
class BaseUserModel(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True) # to be migrated to a cloud storage later
    language_preference = models.CharField(max_length=10, default='en')
    theme_preference = models.CharField(max_length=10, default='light')

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.user_type}"

class UserKYC(BaseKYCModel):
    user = models.OneToOneField(BaseUserModel, on_delete=models.CASCADE, related_name='user_kyc')

    def __str__(self):
        return f"KYC for {self.user.username} - Verified: {self.verified}"