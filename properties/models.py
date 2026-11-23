from django.db import models


class Listing(models.Model):
    STATUS_CHOICES = [
        ("AVAILABLE", "Available"),
        ("PENDING", "Pending"),
        ("SOLD", "Sold"),
    ]
    HOME_TYPE_CHOICES = [
        ("HOUSE", "House"),
        ("CONDO", "Condo"),
        ("TOWNHOUSE", "Townhouse"),
        ("MULTI", "Multi-family"),
        ("LAND", "Land"),
    ]

    address = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField()
    features = models.TextField(blank=True)
    home_type = models.CharField(max_length=20, choices=HOME_TYPE_CHOICES)
    neighborhood = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="AVAILABLE")
    photo_1 = models.ImageField(upload_to="listings/")
    photo_2 = models.ImageField(upload_to="listings/", blank=True)
    photo_3 = models.ImageField(upload_to="listings/", blank=True)
    photo_4 = models.ImageField(upload_to="listings/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address