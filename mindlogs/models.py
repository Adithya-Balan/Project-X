from django.db import models
from myapp.models import userinfo
from django.utils.crypto import get_random_string
from django.db.models import F

BASE62_ALPHABET = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def generate_base62_id(length=8):
    return get_random_string(length=length, allowed_chars=BASE62_ALPHABET)

def generate_unique_signature():
    while True:
        sig = f"sig-{generate_base62_id()}"
        if not MindLog.objects.filter(sig=sig).exists():
            return sig

class MindLog(models.Model):
    user = models.ForeignKey(userinfo, on_delete=models.CASCADE, related_name='mind_logs')
    content = models.TextField(max_length=280)
    neuro_color = models.CharField(max_length=20, default='green', null=True, blank=True) 
    latency = models.PositiveIntegerField(default=180)
    snap_shot = models.ImageField(upload_to='log_snap_shot', blank=True, null=True)
    code_snippet = models.TextField(max_length=1000, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    total_views = models.PositiveIntegerField(default=0) 
    
    # Unique signature
    sig = models.CharField(max_length=20, unique=True, default=generate_unique_signature)
    
    # Cloning
    original_log = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, related_name="clones")

    # Reactions
    clone_count = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(userinfo, related_name="liked_logs", blank=True)
    
    def is_clone(self):
        return self.original_log is not None
    
    def save(self, *args, **kwargs):
        # If the log is a clone, we remove the color
        if self.original_log and self.neuro_color:
            self.neuro_color = None
        elif not self.original_log and not self.neuro_color:
            self.neuro_color = "green"  # ensure original logs get default

        super().save(*args, **kwargs)
        
    def total_likes(self):
        return self.likes.count()
    
    def increment_view_count(self):
        MindLog.objects.filter(pk=self.pk).update(total_views=F('total_views') + 1)

    def __str__(self):
        return f"{self.user.user.username} ▸ {self.sig}"
    

