from django.db import models
import uuid
from django.contrib.auth.models import User
from . import userinfo
from django.urls import reverse


# Create your models here.    
class organization(models.Model):
    ORGANIZATION_TYPES = [
        ('Private', 'Private Company'),
        ('Open', 'Open Organization'),
        ('Club Groups', 'Club/Group'),
        ('Startup', 'Startup'),
        ('NonProfit', 'Non-Profit Organization'), 
        ('Gov', 'Government Institution'),  
        ('Education', 'Educational Institution'), 
        ('Research Lab', 'Research Lab'), 
    ]
    
    INDUSTRY_CHOICES = [
    ('Software & IT Services', 'Software & IT Services'),
    ('Artificial Intelligence & Machine Learning', 'Artificial Intelligence & Machine Learning'),
    ('Cloud Computing & Infrastructure', 'Cloud Computing & Infrastructure'),
    ('Cybersecurity', 'Cybersecurity'),
    ('Blockchain, Crypto & Web3', 'Blockchain, Crypto & Web3'),
    ('Game Development', 'Game Development'),
    ('Financial Technology (Fintech)', 'Financial Technology (Fintech)'),
    ('Education Technology', 'Education Technology'),
    ('Healthcare & Medical Technology', 'Healthcare & Medical Technology'),
    ('Hardware & Electronics', 'Hardware & Electronics'),
    ('Telecommunications', 'Telecommunications'),
    ('E-commerce & Retail Tech', 'E-commerce & Retail Tech'),
    ('Marketing & Advertising Technology', 'Marketing & Advertising Technology'),
    ('Media & Entertainment', 'Media & Entertainment'),
    ('Automotive & Mobility Tech', 'Automotive & Mobility Tech'),
    ('Aerospace & Defense', 'Aerospace & Defense'),
    ('IoT, Robotics & Automation', 'IoT, Robotics & Automation'),
    ('GreenTech & Sustainable Energy', 'GreenTech & Sustainable Energy'),
    ('Augmented Reality & Virtual Reality', 'Augmented Reality & Virtual Reality'),

    # Government & Public Sector
    ('Government & Public Sector', 'Government & Public Sector'),
    ('Defense & Military', 'Defense & Military'),
    ('Law Enforcement & Security', 'Law Enforcement & Security'),
    ('Public Transportation', 'Public Transportation'),
    ('Public Health & Safety', 'Public Health & Safety'),

    # Education & Research
    ('Higher Education & Universities', 'Higher Education & Universities'),
    ('K-12 Schools & Educational Institutions', 'K-12 Schools & Educational Institutions'),
    ('Research & Development', 'Research & Development'),

    # Clubs & Communities
    ('Tech Clubs & Developer Communities', 'Tech Clubs & Developer Communities'),
    ('Cultural, Arts & Sports Organizations', 'Cultural, Arts & Sports Organizations'),
    ('Social & Networking Clubs', 'Social & Networking Clubs'),

    # Non-Profits & NGOs
    ('Non-Profit & Humanitarian Organizations', 'Non-Profit & Humanitarian Organizations'),
    ('Environmental & Sustainability', 'Environmental & Sustainability'),

    # Business & Consulting
    ('Startup & Entrepreneurship', 'Startup & Entrepreneurship'),
    ('IT & Business Consulting', 'IT & Business Consulting'),
    ('Venture Capital & Investment', 'Venture Capital & Investment'),
    ('Legal & Compliance Services', 'Legal & Compliance Services'),
    ('Supply Chain & Logistics', 'Supply Chain & Logistics'),
    ('Real Estate & Property Management', 'Real Estate & Property Management'),
    ('Manufacturing & Industrial Technology', 'Manufacturing & Industrial Technology'),

    # Miscellaneous
    ('Agriculture & Food Tech', 'Agriculture & Food Tech'),
    ('Human Resources & Talent Management', 'Human Resources & Talent Management'),
    ('Journalism & Publishing', 'Journalism & Publishing'),
    ('Entertainment & Performing Arts', 'Entertainment & Performing Arts'),
    ('Religious Organizations', 'Religious Organizations'),
    ('Hospitality & Tourism', 'Hospitality & Tourism'),
    ('Other', 'Other'),
]

    user = models.ForeignKey(User, related_name='organization', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=250)
    description = models.TextField()
    logo = models.ImageField(upload_to="organization_logo", blank=True, default='organization_logo/organization_logo.svg')
    website = models.URLField(null=True, blank=True)
    industry = models.CharField(max_length=200, choices=INDUSTRY_CHOICES, default='TechClub')
    location = models.CharField(max_length=255, blank=True, null=True)
    organization_type = models.CharField(max_length=50, choices=ORGANIZATION_TYPES, default='Private')
    founded_date = models.DateField(null=True, blank=True)
    contact_email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=14, blank=True, null=True)
    github = models.URLField(blank=True, null=True)  
    linkedin = models.URLField(blank=True, null=True) 
    twitter = models.URLField(blank=True, null=True) 
    discord = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    followers = models.ManyToManyField(userinfo, related_name='followed_organization', blank=True)
    
    def __str__(self):
        return f"{self.id} {self.name }"

    def get_absolute_url(self):
        return reverse("organization_detail", kwargs={"id": self.pk})
    
    def is_followed_by(self, userinfo):
        return self.followers.filter(id=userinfo.id).exists()
    
    def get_followers(self):
        return self.followers.all()
    