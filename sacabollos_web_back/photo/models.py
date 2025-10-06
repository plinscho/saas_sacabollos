from django.db import models

# Create your models here.
from django.db import models
import uuid
import os

def upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('photos/', filename)

class Photo(models.Model):
    file = models.ImageField(upload_to=upload_to)
    portfolio_item = models.ForeignKey('portfolio_item.PortfolioItem', on_delete=models.CASCADE, null=True, blank=True, related_name='photos')
    alt_text = models.CharField(max_length=200, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Photo {self.id}"