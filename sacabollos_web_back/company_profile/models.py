from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    address = models.TextField()
    location = models.ForeignKey('locations.Location', on_delete=models.SET_NULL, null=True, blank=True)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name