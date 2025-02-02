from django.db import models
import uuid
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.    
class organization(models.Model):
    ORGANIZATION_TYPES = [
        ('Private', 'Private Company'),
        ('Open', 'Open Organization'),
        ('Club', 'Club/Group'),
    ]
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=1000)
    logo = models.ImageField(upload_to="organization_logo", height_field=None, width_field=None)
    website = models.URLField(null=True, blank=True)
    industry = models.CharField(max_length=100)
    location = models.CharField(max_length=255, blank=True, null=True)
    organization_type = models.CharField(max_length=50, choices=ORGANIZATION_TYPES, default='Private')
    founded_date = models.DateField(auto_now_add=True, null=True, blank=True)
    contact_email = models.EmailField(null=True, blank=True)
    
    def __str__(self):
        return self.name

    