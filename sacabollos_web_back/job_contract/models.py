from django.db import models

# Create your models here.
from django.db import models

class JobContract(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('finished', 'Finished'),
        ('cancelled', 'Cancelled'),
    ]

    job = models.OneToOneField('job_offer.JobOffer', on_delete=models.CASCADE)
    chapista_profile = models.ForeignKey('chapista_profile.ChapistaProfile', on_delete=models.CASCADE)
    company = models.ForeignKey('company_profile.CompanyProfile', on_delete=models.CASCADE)
    agreed_price = models.DecimalField(max_digits=8, decimal_places=2)
    agreed_time_hours = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contract: {self.job.title}"