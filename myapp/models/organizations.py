from django.db import models
from django.db.models import Count, Sum
from django.contrib.auth.models import User
from . import userinfo
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from .filter import Industry


# Create your models here.    
class organization(models.Model):
    ORGANIZATION_TYPES = [
        ('Private', 'Private Company'),
        ('Open', 'Open Organization'),
        ('Club-Groups', 'Club/Group'),
        ('Startup', 'Startup'),
        ('NonProfit', 'Non-Profit Organization'), 
        ('Gov', 'Government Institution'),  
        ('Education', 'Educational Institution'), 
        ('Research Lab', 'Research Lab'), 
    ]
    user = models.ForeignKey(User, related_name='organization', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=250)
    description = models.TextField()
    logo = models.ImageField(upload_to="organization_logo", blank=True, default='organization_logo/org-logo.png')
    website = models.URLField(null=True, blank=True)
    industry = models.ForeignKey(Industry, on_delete=models.SET_NULL, null=True, related_name='organizations')
    location = models.CharField(max_length=255, blank=True, null=True)
    organization_type = models.CharField(max_length=50, choices=ORGANIZATION_TYPES, default='Private')
    founded_date = models.DateField(null=True, blank=True)
    contact_email = models.EmailField(null=True, blank=True)
    phone = PhoneNumberField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)  
    linkedin = models.URLField(blank=True, null=True) 
    twitter = models.URLField(blank=True, null=True) 
    discord = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    followers = models.ManyToManyField(userinfo, related_name='followed_organization', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    profile_views_followers = models.IntegerField(default=0)
    profile_views_nonfollowers = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.id} {self.name }"

    def get_absolute_url(self):
        return reverse("organization_detail", kwargs={"id": self.pk})
    
    def is_followed_by(self, userinfo):
        return self.followers.filter(id=userinfo.id).exists()
    
    def get_followers(self):
        return self.followers.all()
    
    def get_total_likes(self):
        tot_likes = self.all_post.annotate(num_likes=Count('likes')).aggregate(total_likes=Sum('num_likes'))['total_likes'] or 0
        return tot_likes
    
    def get_organization_type_filters():
        ORGANIZATION_TYPES = [
        ('Private', 'Private Company'),
        ('Open', 'Open Organization'),
        ('Club-Groups', 'Club/Group'),
        ('Startup', 'Startup'),
        ('NonProfit', 'Non-Profit Organization'), 
        ('Gov', 'Government Institution'),  
        ('Education', 'Educational Institution'), 
        ('Research Lab', 'Research Lab'), 
    ]
        """
        Returns organization types in a list of dictionaries for frontend filtering.
        """
        return [{'value': value, 'label': label} for value, label in ORGANIZATION_TYPES]

    