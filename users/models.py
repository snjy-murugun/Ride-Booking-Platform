from django.contrib.auth.models import AbstractUser
from django.db import models   

# Create your models here.
class user(AbstractUser):
    ROLE_CHOICES = [('rider', 'Rider'),
                    ('driver', 'Driver'),
                    ('admin', 'Admin' ),]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='rider')
    
    phone_number_field = models.CharField(max_length=15, blank=True, null=True)
    
    is_available = models.BooleanField(default=False)
    
    def __str__self():
        return f"{self.username} ({self.role})"
    