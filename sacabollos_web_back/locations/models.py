from django.db import models

# Create your models here.
from django.db import models

class Location(models.Model):
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='Spain')
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    lat = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    lng = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['city', 'province', 'country']

    def __str__(self):
        return f"{self.city}, {self.province}, {self.country}"