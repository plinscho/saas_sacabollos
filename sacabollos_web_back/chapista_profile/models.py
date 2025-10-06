from django.db import models
from django.contrib.auth.models import User

class ChapistaProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    servicios_ofrecidos = models.JSONField(default=list, help_text="Tags/specialties as JSON array")
    precio_hora_estimado = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    rating_promedio = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    location = models.ForeignKey('locations.Location', on_delete=models.SET_NULL, null=True, blank=True)
    disponibilidad = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Chapista: {self.display_name}"