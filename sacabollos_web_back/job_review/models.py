from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class JobReview(models.Model):
    job = models.ForeignKey('job_contract.JobContract', on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['job', 'from_user', 'to_user']

    def __str__(self):
        return f"Review: {self.rating}★ from {self.from_user.username} to {self.to_user.username}"