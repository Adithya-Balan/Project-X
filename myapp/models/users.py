from django.db import models
import uuid
from django.contrib.auth.models import User
from django.urls import reverse
from .filter import skill, Domain, user_status
from phonenumber_field.modelfields import PhoneNumberField

class userinfo(models.Model):
    GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('NB', 'Non-Binary'),
    ('O', 'Other'),
    ('N', 'Prefer not to say'),
]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='info')
    bio = models.CharField(max_length=100, blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    contact_email = models.EmailField(max_length=255, blank=True, null=True)
    about_user = models.TextField(max_length=1000, blank=True, null=True) 
    profile_image = models.ImageField(upload_to='user_profile_img', height_field=None, default='user_profile_img/profile.webp')
    location = models.CharField(max_length=50, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    gender = models.CharField(max_length=25, null=True, blank=True, choices=GENDER_CHOICES)
    status = models.ForeignKey(user_status, related_name='developers', on_delete=models.SET_NULL, null=True)

    github = models.URLField(blank=True, null=True)  
    linkedin = models.URLField(blank=True, null=True) 
    twitter = models.URLField(blank=True, null=True) 
    stackoverflow = models.URLField(blank=True, null=True) 
    
    skills = models.ManyToManyField(skill, related_name='users', blank=True)
    domains = models.ManyToManyField(Domain, verbose_name="developers", blank=True)
    years_of_experience = models.PositiveIntegerField(blank=True, null=True)
    availability = models.CharField(max_length=50, choices=[
        ('Available for collaboration', 'Available for collaboration'),
        ('Open to part-time collaboration', 'Open to part-time collaboration'),
        ('Open to freelance collaboration', 'Open to freelance collaboration'),
        ('Unavailable', 'Unavailable'),
    ], blank=True, null=True)
    # mood = models.CharField(max_length=50, blank=True, null=True)
    timezone = models.CharField(max_length=100, default='UTC')
    
    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("user_info_detail", kwargs={"pk": self.pk})
    
    #following methods:
    def follow(self, other_user):
        if not self.is_following(other_user):
            follow.objects.create(follower = self, following=other_user)
    
    def unfollow(self, other_user):
        if self.is_following(other_user):
            follow.objects.filter(follower = self, following = other_user).delete()
    
    def is_following(self, other_user):
        return follow.objects.filter(follower = self, following = other_user).exists()
    
    def get_followers(self):
        return userinfo.objects.filter(following__following=self).order_by('-following__created_at')
    
    def get_following(self):
        return userinfo.objects.filter(followers__follower = self).order_by('-followers__created_at')


class education(models.Model):
    user = models.OneToOneField(userinfo, on_delete=models.CASCADE, related_name='education')
    name = models.CharField(max_length=100)
    degree = models.CharField(max_length=255, blank=True, null=True)
    field_of_study = models.CharField(max_length=255, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    till_now = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.id}-{self.name}"
    
class current_position(models.Model):
    user = models.OneToOneField(userinfo, on_delete=models.CASCADE, related_name='current_position')
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)  
    till_now = models.BooleanField(default=False)
    
    
    def __str__(self):
        return f"{self.id}-{self.name}"
    
class user_project(models.Model):
    user = models.ForeignKey(userinfo, related_name='projects', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    url = models.URLField(blank=True, null=True)
    repo_link = models.URLField(blank=True, null=True)
    tech_stack = models.ManyToManyField(skill, related_name='user_projects', blank=True)
    media = models.FileField(upload_to="user-project-files", blank=True, null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(blank=True, null=True)


class experience(models.Model): #Auto create.
    user = models.ForeignKey(userinfo, related_name='experiences', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    role = models.TextField(max_length=500)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    till_now = models.BooleanField(default=False)
    
class follow(models.Model):
    follower = models.ForeignKey(userinfo, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(userinfo, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.follower.user.username} {self.following.user.username}"
    
    class meta:
        unique_together = ('follower', 'following') 
        
