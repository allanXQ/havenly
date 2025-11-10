from django.db import models
from common.models import BaseModel

# Create your models here.
class Site(BaseModel):
    address = models.CharField(max_length=255, blank=False, null=False)
    city = models.CharField(max_length=100, blank=False, null=False)
    state = models.CharField(max_length=100, blank=False, null=False)
    zip_code = models.CharField(max_length=20, blank=False, null=False)
    country = models.CharField(max_length=100, blank=False, null=False)
    owner_organization = models.ForeignKey('organizations.Organizations', on_delete=models.CASCADE)
    location_coordinates = models.CharField(max_length=100, blank=True, null=True)
    images = models.ImageField(upload_to='site_images/', blank=True, null=True) # to be migrated to a cloud storage later


    def __str__(self):
        return f"{self.address}, {self.city}, {self.state}, {self.country}"
    
class Building(BaseModel):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='buildings')
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    number_of_floors = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return f"{self.name} at {self.site.address}"