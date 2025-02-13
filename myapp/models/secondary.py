from django.db import models
from django.urls import reverse
from .users import userinfo
from .filter import Domain, skill
from .organizations import organization
    
class projects(models.Model):
    TYPES = [
    ('O', 'Open-Source'),
    ('F', 'Freelance'),
    ('P', 'Paid'),
    ('L', 'Learning')
]
    LEVELS = [
        ('B', 'Beginner'),
        ('I', 'Intermediate'),
        ('E', 'Expert')
    ]
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="project/thumbnail", height_field=None, width_field=None)
    type = models.CharField(max_length=1, blank=True, null= True, choices=TYPES)
    creator = models.ForeignKey(userinfo, related_name='created_projects', on_delete=models.CASCADE)
    members = models.ManyToManyField(userinfo , related_name='joined_projects', blank=True)
    file = models.FileField(upload_to='project/files', blank=True, null=True)
    video = models.FileField(upload_to="project/videos", blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    github_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    skill_needed = models.ManyToManyField(skill, related_name='projects')
    domain = models.ForeignKey(Domain, related_name='projects', on_delete=models.SET_NULL, null=True)
    level = models.CharField(max_length=1, blank=True, null= True, choices=LEVELS)
    
    class Meta:
        verbose_name_plural = "projects"
        
    def __str__(self):
        return self.title
    
    def tot_member(self):
        return self.members.all().count()
    
    def tot_comments(self):
        comments = self.forum.all()
        total_replies = sum(comment.replies.count() for comment in comments)
        return comments.count() + total_replies
    
class project_comment(models.Model):
    user = models.ForeignKey(userinfo, related_name='project_comments', on_delete=models.CASCADE)
    content = models.TextField()
    project = models.ForeignKey(projects, related_name="forum", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
         return f"{self.id} Comment by {self.user.user.username} on {self.project.title}"
     
    
class project_reply(models.Model):
    user = models.ForeignKey(userinfo, related_name='project_replies', on_delete=models.CASCADE)
    comment = models.ForeignKey(project_comment, related_name='replies', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Reply by {self.user.user.username} to {self.comment.user.user.username}'s comment"
    
    class Meta:
        verbose_name_plural = "project_reply"

# User-Posts
class post(models.Model):
    content = models.TextField()
    file = models.FileField(upload_to='user-posts')
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(userinfo, related_name='liked_posts', blank=True)
    
    # Either a User OR an Organization can be the author
    user = models.ForeignKey(userinfo, related_name='all_post', on_delete=models.CASCADE, null=True, blank=True)
    Organization = models.ForeignKey(organization, related_name='all_post', on_delete=models.CASCADE, null=True, blank=True)
    # post_type = models.CharField(max_length=10, choices=POST_TYPE, default='img')
    def __str__(self):
        return f"Post by {self.user or self.organization} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    def total_likes(self):
        return self.likes.count()
    
    def tot_comments(self):
        return self.comments.count()
    
class post_comments(models.Model):
    user = models.ForeignKey(userinfo, related_name='post_comments', on_delete=models.CASCADE)
    Post = models.ForeignKey(post, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.user} on {self.Post.id}"
    
    class Meta:
        verbose_name_plural = "Post comments"
        ordering = ['-created_at']  
    
    
class event(models.Model):
    EVENT_TYPE_CHOICES = [
        ('webinar', 'Webinar'),
        ('workshop', 'Workshop'),
        ('conference', 'Conference'),
        ('meetup', 'Meetup'),
        ('hackathon', 'Hackathon'),
        ('other', 'Other'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    organization = models.ForeignKey(organization, related_name='events', on_delete=models.CASCADE)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES, default='other')
    location = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    banner = models.ImageField(upload_to='events', help_text="Optional image for the event.")
    
    def __str__(self):
        return f"{self.title} ({self.get_event_type_display()})"
    
class SavedItem(models.Model):
    user = models.OneToOneField(userinfo, related_name='saved_items', on_delete=models.CASCADE)
    posts = models.ManyToManyField(post, related_name='saved_by_posts', blank=True)
    project = models.ManyToManyField(projects, related_name='saved_by_projects', blank=True)
    events = models.ManyToManyField(event, related_name='saved_by_events', blank=True) 
    saved_at = models.DateTimeField(auto_now_add=True)
    
    def toggle_project(self, project_obj):
        if project_obj in self.project.all():
            self.project.remove(project_obj)
            return False  # Indicates the project was unsaved.
        else:
            self.project.add(project_obj)
            return True   # Indicates the project was saved.

    def __str__(self):
        return f"Saved items for {self.user}"
    