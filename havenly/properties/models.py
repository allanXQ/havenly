from django.db import models
from common.models import BaseModel
from django.core.exceptions import ValidationError

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
class Floor(BaseProperty):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='floors')

    def __str__(self):
        return f"{self.name} in {self.building.name}"
    
class Unit(BaseProperty):
    availability_choices = [
        ('review', 'Under Review'),
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Under Maintenance'),
    ]
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name='units')
    unit_number = models.CharField(max_length=50, blank=False, null=False)
    square_footage = models.PositiveIntegerField(blank=True, null=True)
    number_of_bedrooms = models.PositiveIntegerField(blank=True, null=True)
    number_of_bathrooms = models.PositiveIntegerField(blank=True, null=True)
    availability_status = models.CharField(max_length=20, choices=availability_choices, default='review')

    def __str__(self):
        return f"Unit {self.unit_number} on {self.floor.name} in {self.floor.building.name}"
class Amenity(BaseProperty):
    CATEGORY_CHOICES = [
        ('recreation', 'Recreation'),
        ('security', 'Security'),
        ('utilities', 'Utilities'),
        ('parking', 'Parking'),
        ('accessibility', 'Accessibility'),
        ('entertainment', 'Entertainment'),
        ('wellness', 'Wellness'),
        ('connectivity', 'Connectivity'),
        ('outdoor', 'Outdoor'),
        ('storage', 'Storage'),
        ('other', 'Other'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    icon = models.CharField(max_length=50, blank=True, help_text="Icon class or identifier")
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'amenities'
        verbose_name = 'Amenity'
        verbose_name_plural = 'Amenities'
        ordering = ['category', 'name']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class AmenityAssignment(BaseProperty):
    """
    Junction table for assigning amenities to different property levels.
    Each assignment must be to exactly one level (site, building, floor, or unit).
    """
    amenity = models.ForeignKey(
        Amenity,
        on_delete=models.CASCADE,
        related_name='assignments'
    )
    
    # Property level foreign keys (exactly one must be set)
    site = models.ForeignKey(
        'Site',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='amenity_assignments'
    )
    building = models.ForeignKey(
        'Building',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='amenity_assignments'
    )
    floor = models.ForeignKey(
        'Floor',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='amenity_assignments'
    )
    unit = models.ForeignKey(
        'Unit',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='amenity_assignments'
    )
    
    notes = models.TextField(blank=True, help_text="Additional context about this amenity assignment")
    class Meta:
        db_table = 'amenity_assignments'
        verbose_name = 'Amenity Assignment'
        verbose_name_plural = 'Amenity Assignments'
        indexes = [
            models.Index(fields=['amenity', 'site']),
            models.Index(fields=['amenity', 'building']),
            models.Index(fields=['amenity', 'floor']),
            models.Index(fields=['amenity', 'unit']),
            models.Index(fields=['created_at']),
        ]
        constraints = [
            # Ensure exactly one property level is set
            models.CheckConstraint(
                check=(
                    models.Q(site__isnull=False, building__isnull=True, floor__isnull=True, unit__isnull=True) |
                    models.Q(site__isnull=True, building__isnull=False, floor__isnull=True, unit__isnull=True) |
                    models.Q(site__isnull=True, building__isnull=True, floor__isnull=False, unit__isnull=True) |
                    models.Q(site__isnull=True, building__isnull=True, floor__isnull=True, unit__isnull=False)
                ),
                name='amenity_assignment_exactly_one_level'
            ),
        ]
        # Prevent duplicate assignments at the same level
        unique_together = [
            ('amenity', 'site'),
            ('amenity', 'building'),
            ('amenity', 'floor'),
            ('amenity', 'unit'),
        ]

    def clean(self):
        """
        Validate that exactly one property level is set.
        """
        levels_set = sum([
            self.site_id is not None,
            self.building_id is not None,
            self.floor_id is not None,
            self.unit_id is not None,
        ])
        
        if levels_set == 0:
            raise ValidationError("At least one property level (site, building, floor, or unit) must be specified.")
        
        if levels_set > 1:
            raise ValidationError("Only one property level can be specified per assignment.")

    def save(self, *args, **kwargs):
        """
        Override save to run validation.
        """
        self.full_clean()
        super().save(*args, **kwargs)

    def get_assignment_level(self):
        """
        Returns the level name and object this amenity is assigned to.
        """
        if self.site:
            return ('site', self.site)
        elif self.building:
            return ('building', self.building)
        elif self.floor:
            return ('floor', self.floor)
        elif self.unit:
            return ('unit', self.unit)
        return (None, None)

    def __str__(self):
        level, obj = self.get_assignment_level()
        return f"{self.amenity.name} → {level}: {obj}"
class Listing(BaseProperty):
    availability_status_choices = [
        ('available', 'Available'),
        ('rented', 'Rented'),
        ('maintenance', 'Under Maintenance'),
    ]
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='listings')
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    availability_status = models.CharField(max_length=50, choices=availability_status_choices, default='available')

    def __str__(self):
        return f"Listing for {self.unit} - {self.price}"