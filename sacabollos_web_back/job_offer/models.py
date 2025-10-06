from django.db import models

# Create your models here.
from django.db import models

class JobOffer(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('assigned', 'Assigned'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ]

    company = models.ForeignKey('company_profile.CompanyProfile', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.ForeignKey('locations.Location', on_delete=models.SET_NULL, null=True, blank=True)
    budget_min = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    budget_max = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    estimated_time_hours = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    tags = models.JSONField(default=list, help_text="Categories/tags as JSON array")
    deadline = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.company.company_name}"