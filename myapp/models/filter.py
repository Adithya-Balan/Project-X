from django.db import models
from django.urls import reverse

class CringeBadge(models.Model):
    name = models.CharField(max_length=50, unique=True) 
    description = models.TextField()
    emoji = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.emoji} {self.name}"

class skill(models.Model): #Skills
    category_choices = [
    ('Programming Language', 'Programming Language'),
    ('Framework', 'Framework'),
    ('Tool', 'Tool'),
    ('Database', 'Database'),
    ('Cloud Platform', 'Cloud Platform'),
    ('Version Control', 'Version Control'),
    ('DevOps', 'DevOps'),
    ('UI/UX Design', 'UI/UX Design'),
    ('Machine Learning', 'Machine Learning'),
    ('Web Development', 'Web Development')
]   
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50, choices=category_choices, default='Programming Language')
    description = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.name

class Domain(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
class user_status(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    
    class Meta:
        verbose_name_plural = "user_status"
        
    def __str__(self):
        return self.name
    
class Industry(models.Model): #Filter of industry in Organization
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name