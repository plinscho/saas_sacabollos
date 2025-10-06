from django.db import models

# Create your models here.
class JobProposal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    job = models.ForeignKey('job_offer.JobOffer', on_delete=models.CASCADE, related_name='proposals')
    chapista_profile = models.ForeignKey('chapista_profile.ChapistaProfile', on_delete=models.CASCADE)
    message = models.TextField()
    proposed_price = models.DecimalField(max_digits=8, decimal_places=2)
    proposed_time_hours = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['job', 'chapista_profile']

    def __str__(self):
        return f"Proposal by {self.chapista_profile.display_name} for {self.job.title}"