from django.db import models
from common.models import BaseModel

# Create your models here.

class BaseProperty(BaseModel):
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)


    def get_upload_path(instance, filename):
        return f'{instance.__class__.__name__.lower()}_images/{filename}'
    images = models.ImageField(upload_to=get_upload_path, blank=True, null=True) # to be migrated to a cloud storage later
    
    class Meta:
        abstract = True

class Site(BaseProperty):
    address = models.CharField(max_length=255, blank=False, null=False)
    city = models.CharField(max_length=100, blank=False, null=False)
    state = models.CharField(max_length=100, blank=False, null=False)
    zip_code = models.CharField(max_length=20, blank=False, null=False)
    country = models.CharField(max_length=100, blank=False, null=False)
    owner_organization = models.ForeignKey('organizations.Organizations', on_delete=models.CASCADE, related_name='sites')
    location_coordinates = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.address}, {self.city}, {self.state}, {self.country}"

class Building(BaseProperty):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='buildings')

    def __str__(self):
        return f"{self.name} at {self.site.address}"

class Amenities(BaseProperty):
    level_id = models.CharField(max_length=50, blank=True, null=True) # section identifier, can be site id, building id etc

    def __str__(self):
        return f"{self.name} in {self.building.name}"
class Floor(BaseProperty):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='floors')

    def __str__(self):
        return f"{self.name} in {self.building.name}"
    
class Unit(BaseProperty):
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name='units')
    unit_number = models.CharField(max_length=50, blank=False, null=False)
    square_footage = models.PositiveIntegerField(blank=True, null=True)
    number_of_bedrooms = models.PositiveIntegerField(blank=True, null=True)
    number_of_bathrooms = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"Unit {self.unit_number} on {self.floor.name} in {self.floor.building.name}"