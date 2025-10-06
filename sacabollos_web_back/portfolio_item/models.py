from django.db import models

# Create your models here.
from django.db import models

class PortfolioItem(models.Model):
    chapista_profile = models.ForeignKey('chapista_profile.ChapistaProfile', on_delete=models.CASCADE, related_name='portfolio')
    title = models.CharField(max_length=200)
    description = models.TextField()
    tags = models.JSONField(default=list)
    date_completed = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_completed']

    def __str__(self):
        return f"{self.title} - {self.chapista_profile.display_name}"