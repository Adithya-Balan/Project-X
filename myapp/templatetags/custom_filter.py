from django import template
from myapp.models import follow
import urllib.parse

register = template.Library()

@register.filter
def is_following(user,otheruser):
    return follow.objects.filter(follower = user, following = otheruser).exists()
