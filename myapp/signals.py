from django.dispatch import receiver
from allauth.account.signals import user_signed_up, user_logged_in
from django.contrib.auth.models import User
from myapp.models import userinfo, current_position, education, SavedItem 

@receiver(user_signed_up)
@receiver(user_logged_in)
def create_user_profile(sender, request, user, **kwargs):
    """
    Automatically create user-related objects after login or signup.
    """
    # Check if userinfo already exists (to prevent duplicate creation)
    if not userinfo.objects.filter(user=user).exists():
        userinfo.objects.create(user=user)

    # Ensure user.info exists before creating related models
    if hasattr(user, 'info'):
        current_position.objects.get_or_create(user=user.info)
        education.objects.get_or_create(user=user.info)
        SavedItem.objects.get_or_create(user=user.info)