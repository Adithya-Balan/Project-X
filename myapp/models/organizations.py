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
        ('Club', 'Club/Group'),
        ('Startup', 'Startup'),
        ('NonProfit', 'Non-Profit Organization'), 
        ('Gov', 'Government Institution'),  
        ('Education', 'Educational Institution'), 
        ('Research', 'Research Lab'), 
    ]
    
    INDUSTRY_CHOICES = [
    # Technology & Software
    ('Software', 'Software & IT Services'),
    ('AI_ML', 'Artificial Intelligence & Machine Learning'),
    ('Cloud', 'Cloud Computing & Infrastructure'),
    ('Cybersecurity', 'Cybersecurity'),
    ('Blockchain', 'Blockchain, Crypto & Web3'),
    ('GameDev', 'Game Development'),
    ('Fintech', 'Financial Technology (Fintech)'),
    ('EdTech', 'Education Technology'),
    ('HealthTech', 'Healthcare & Medical Technology'),
    ('Hardware', 'Hardware & Electronics'),
    ('Telecom', 'Telecommunications'),
    ('Ecommerce', 'E-commerce & Retail Tech'),
    ('Marketing', 'Marketing & Advertising Technology'),
    ('Media', 'Media & Entertainment'),
    ('Automotive', 'Automotive & Mobility Tech'),
    ('Aerospace', 'Aerospace & Defense'),
    ('IoT_Robotics', 'IoT, Robotics & Automation'),
    ('GreenTech', 'GreenTech & Sustainable Energy'),
    ('AR_VR', 'Augmented Reality & Virtual Reality'),
    
    # Government & Public Sector
    ('Gov', 'Government & Public Sector'),
    ('Defense', 'Defense & Military'),
    ('LawEnforcement', 'Law Enforcement & Security'),
    ('PublicTransport', 'Public Transportation'),
    ('PublicHealth', 'Public Health & Safety'),

    # Education & Research
    ('HigherEd', 'Higher Education & Universities'),
    ('K12', 'K-12 Schools & Educational Institutions'),
    ('Research', 'Research & Development'),
    
    # Clubs & Communities
    ('TechClub', 'Tech Clubs & Developer Communities'),
    ('Cultural_Sports', 'Cultural, Arts & Sports Organizations'),
    ('SocialClub', 'Social & Networking Clubs'),

    # Non-Profits & NGOs
    ('NonProfit', 'Non-Profit & Humanitarian Organizations'),
    ('Environmental', 'Environmental & Sustainability'),
    
    # Business & Consulting
    ('Startup', 'Startup & Entrepreneurship'),
    ('Consulting', 'IT & Business Consulting'),
    ('VentureCapital', 'Venture Capital & Investment'),
    ('Legal', 'Legal & Compliance Services'),
    ('SupplyChain', 'Supply Chain & Logistics'),
    ('RealEstate', 'Real Estate & Property Management'),
    ('Manufacturing', 'Manufacturing & Industrial Technology'),

    # Miscellaneous
    ('Agritech', 'Agriculture & Food Tech'),
    ('HumanResources', 'Human Resources & Talent Management'),
    ('Journalism', 'Journalism & Publishing'),
    ('Entertainment', 'Entertainment & Performing Arts'),
    ('Religion', 'Religious Organizations'),
    ('Hospitality', 'Hospitality & Tourism'),
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
        return reverse("organization_page", kwargs={"id": self.pk})
    
    def is_followed_by(self, userinfo):
        return self.followers.filter(id=userinfo.id).exists()
    
    def get_followers(self):
        return self.followers.all()
    