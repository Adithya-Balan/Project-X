from django.db import models
from django.urls import reverse
from .users import userinfo
from .filter import Domain, skill
    
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
    