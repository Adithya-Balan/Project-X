from django import template
from myapp.models import follow, organization
import urllib.parse

register = template.Library()

@register.filter
def is_following(user,otheruser):
    return follow.objects.filter(follower = user, following = otheruser).exists()

@register.filter
def is_following_org(userinfo, org):
    return org.followers.filter(id=userinfo.id).exists()

@register.filter
def lstrip(value):
    return value.strip()