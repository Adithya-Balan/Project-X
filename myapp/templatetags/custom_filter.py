from django import template
from myapp.models import follow

register = template.Library()

@register.filter
def is_following(user,otheruser):
    return follow.objects.filter(follower = user, following = otheruser).exists()