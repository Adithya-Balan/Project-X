from django.db import models
from django.urls import reverse
from .users import userinfo
from .filter import Domain, skill
from .organizations import organization
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.timezone import now
    
class projects(models.Model):
    TYPES = [
    ('Open-Source', 'Open-Source'),
    ('Freelance', 'Freelance'),
    ('Paid', 'Paid'),
    ('Learning', 'Learning')
]
    LEVELS = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Expert', 'Expert')
    ]
    title = models.CharField(max_length=100, db_index=True)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to="project/thumbnail", height_field=None, width_field=None)
    type = models.CharField(max_length=50, blank=True, null= True, choices=TYPES)
    creator = models.ForeignKey(userinfo, related_name='created_projects', on_delete=models.CASCADE)
    members = models.ManyToManyField(userinfo , related_name='joined_projects', blank=True)
    file = models.FileField(upload_to='project/files', blank=True, null=True)
    video = models.FileField(upload_to="project/videos", blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    github_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    skill_needed = models.ManyToManyField(skill, related_name='projects')
    domain = models.ForeignKey(Domain, related_name='projects', on_delete=models.SET_NULL, null=True)
    level = models.CharField(max_length=50, blank=True, null= True, choices=LEVELS, db_index=True)
    
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
    ASPECT_CHOICES = [
        ('Original', 'Original'),
        ('1:1', '1:1'),
        ('16:9', '16:9'),
    ]
    content = models.TextField()
    file = models.ImageField(upload_to='user-posts', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(userinfo, related_name='liked_posts', blank=True)
    aspect = models.CharField(max_length=10, choices=ASPECT_CHOICES, default='16:9')
    
    # Either a User OR an Organization can be the author
    user = models.ForeignKey(userinfo, related_name='all_post', on_delete=models.CASCADE, null=True, blank=True)
    Organization = models.ForeignKey(organization, related_name='all_post', on_delete=models.CASCADE, null=True, blank=True)
    # post_type = models.CharField(max_length=10, choices=POST_TYPE, default='img')
    def __str__(self):
        return f"{self.id} Post by {self.user or self.Organization}"
    
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
        ('bootcamp', 'Bootcamp'),
        ('startup Pitch', 'Startup Pitch'),
        ('networking', 'Networking'),
        ('other', 'Other'),
    ]
    EVENT_MODE = [
        ('online', 'online'),
        ('offline', 'offline'),
        ('hybrid', 'Hybrid (Online & Offline)'),
    ]
    title = models.CharField(max_length=255)
    short_description = models.TextField(max_length=255, help_text="A brief overview of the event", null=True)
    description = models.TextField(null=True)
    organization = models.ForeignKey(organization, related_name='events', on_delete=models.CASCADE)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES, default='other')
    location = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    banner = models.ImageField(upload_to='events', help_text="Optional Banner for the event.", blank=True, default='events/default-event-banner.png')
    mode = models.CharField(max_length=50, choices=EVENT_MODE,null=True, blank=True)
    registration_link = models.URLField(blank=True, null=True)   
    
    contact_name = models.CharField(max_length=50, blank=True, null=True)
    contact_email =  models.EmailField(blank=True, null=True)
    contact_phone = PhoneNumberField(blank=True, null=True)
    

    def __str__(self):
        return f"{self.title} ({self.get_event_type_display()})"
    
    def tot_comments(self):
        comments = self.forum.all()
        total_replies = sum(comment.replies.count() for comment in comments)
        return comments.count() + total_replies
    
class event_comment(models.Model):
    user = models.ForeignKey(userinfo, related_name='event_comments', on_delete=models.CASCADE)
    content = models.TextField()
    event = models.ForeignKey(event, related_name="forum", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
         return f"{self.id} Comment by {self.user.user.username} on {self.event.title}"
     
    
class event_reply(models.Model):
    user = models.ForeignKey(userinfo, related_name='event_replies', on_delete=models.CASCADE)
    comment = models.ForeignKey(event_comment, related_name='replies', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Reply by {self.user.user.username} to {self.comment.user.user.username}'s comment"
    
    class Meta:
        verbose_name_plural = "event_replies"
    
class SavedItem(models.Model):
    user = models.OneToOneField(userinfo, related_name='saved_items', on_delete=models.CASCADE)
    posts = models.ManyToManyField(post, related_name='saved_by_posts', blank=True)
    project = models.ManyToManyField(projects, related_name='saved_by_projects', blank=True)
    events = models.ManyToManyField(event, related_name='saved_by_events', blank=True) 
    saved_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Saved items for {self.user}"
    
    def tot_count(self):
        tot_posts = self.posts.all().count()
        tot_projects = self.project.all().count()
        tot_events = self.events.all().count()
        return {'posts': tot_posts, 'projects': tot_projects, 'events': tot_events}
    
class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('like', 'Liked your post'),
        ('comment', 'Commented on your post'),
        ('follow', 'Started following you'),
        ('Join_Project', 'Joined On Your Project'),
        ('project_comment', 'Commented on Your project'),
    )
    user = models.ForeignKey(userinfo, on_delete=models.CASCADE, related_name="notifications")
    sender = models.ForeignKey(userinfo, on_delete=models.CASCADE, related_name="sent_notifications")
    notification_type = models.CharField(choices=NOTIFICATION_TYPES, max_length=50)
    post = models.ForeignKey(post, on_delete=models.CASCADE, null=True, blank=True)
    post_comment = models.ForeignKey(post_comments, on_delete=models.CASCADE, null=True, blank=True) 
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=now)
    
    project = models.ForeignKey(projects, on_delete=models.CASCADE, null=True, blank=True)
    project_comment = models.ForeignKey(project_comment, null=True, blank=True, on_delete=models.CASCADE)
    project_reply = models.ForeignKey(project_reply, on_delete=models.CASCADE, blank=True, null=True)
    
    organization = models.ForeignKey(organization, on_delete=models.CASCADE, null=True, blank=True)  # Organization Follow/Like/Comment

    def __str__(self):
        return f"{self.sender} {self.get_notification_type_display()} {self.user}"

    
    
    