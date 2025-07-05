from django.dispatch import receiver
from allauth.account.signals import user_signed_up, user_logged_in
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, pre_save
from myapp.models import userinfo, current_position, education, SavedItem 
from django.dispatch import receiver
from django.core.files.storage import default_storage
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from .models import projects, post, user_project, userinfo, organization, event as Event

@receiver(post_save, sender=User)
def create_related_user_models(sender, instance, created, **kwargs):
    if created:
        info, _ = userinfo.objects.get_or_create(user=instance)
        current_position.objects.get_or_create(user=info)
        education.objects.get_or_create(user=info)
        SavedItem.objects.get_or_create(user=info)
        
@receiver(user_signed_up)
def handle_new_social_signup(request, user, **kwargs):
    if hasattr(user, 'info'):
        user.info.needs_profile_completion = True
        user.info.save()

# Signal to delete files when a Projects instance is deleted
@receiver(post_delete, sender=projects)
def delete_project_files(sender, instance, **kwargs):
    # Delete video file if it exists
    if instance.video and default_storage.exists(instance.video.name):
        default_storage.delete(instance.video.name)
    # Delete file if it exists
    if instance.file and default_storage.exists(instance.file.name):
        default_storage.delete(instance.file.name)
    # Delete image (thumbnail) file if it exists
    if instance.image and default_storage.exists(instance.image.name):
        default_storage.delete(instance.image.name)


# Signal to delete old files when video or file is updated
@receiver(pre_save, sender=projects)
def delete_old_files_on_update(sender, instance, **kwargs):
    if not instance.pk:  # If this is a new instance, skip
        return

    try:
        # Optimize query to fetch only video and file fields
        old_instance = projects.objects.only('video', 'file').get(pk=instance.pk)
    except projects.DoesNotExist:
        return

    # Check if video has changed
    if old_instance.video and old_instance.video != instance.video and default_storage.exists(old_instance.video.name):
        default_storage.delete(old_instance.video.name)

    # Check if file has changed
    if old_instance.file and old_instance.file != instance.file and default_storage.exists(old_instance.file.name):
        default_storage.delete(old_instance.file.name)
        
    # Check if image (thumbnail) has changed
    if old_instance.image and old_instance.image != instance.image and default_storage.exists(old_instance.image.name):
        default_storage.delete(old_instance.image.name)
        
        
#Events
@receiver(post_delete, sender=Event)
def delete_event_banner(sender, instance, **kwargs):
    # Skip if banner is empty, None, or the default
    if (instance.banner and instance.banner.name and 
        instance.banner.name != instance.banner.field.default):
        if default_storage.exists(instance.banner.name):
            default_storage.delete(instance.banner.name)

@receiver(pre_save, sender=Event)
def delete_old_event_banner(sender, instance, **kwargs):
    if not instance.pk:  # If this is a new instance, skip
        return

    try:
        old_instance = Event.objects.only('banner').get(pk=instance.pk)
    except Event.DoesNotExist:
        return

    # Skip if old banner is empty, None, or the default
    if (old_instance.banner and old_instance.banner.name and 
        old_instance.banner != instance.banner and 
        old_instance.banner.name != old_instance.banner.field.default and 
        default_storage.exists(old_instance.banner.name)):
        default_storage.delete(old_instance.banner.name)
        
# For Posts
@receiver(post_delete, sender=post)
def delete_post_file(sender, instance, **kwargs):
    # Delete file if it exists
    if instance.file and instance.file.name:
        if default_storage.exists(instance.file.name):
            default_storage.delete(instance.file.name)
            
@receiver(post_delete, sender=user_project)
def delete_user_project_media(sender, instance, **kwargs):
    # Delete media file if it exists
    if instance.media and instance.media.name:
        if default_storage.exists(instance.media.name):
            default_storage.delete(instance.media.name)

@receiver(pre_save, sender=userinfo)
def delete_old_userinfo_profile_image(sender, instance, **kwargs):
    if not instance.pk:  # If this is a new instance, skip
        return
    
    try:
        old_instance = userinfo.objects.only('profile_image').get(pk=instance.pk)
    except userinfo.DoesNotExist:
        return
    
    # Skip if old profile_image is empty or the default
    if (old_instance.profile_image and old_instance.profile_image.name and 
        old_instance.profile_image != instance.profile_image and 
        old_instance.profile_image.name != old_instance.profile_image.field.default and 
        default_storage.exists(old_instance.profile_image.name)):
        default_storage.delete(old_instance.profile_image.name)
        
@receiver(post_delete, sender=userinfo)
def delete_userinfo_profile_image_on_delete(sender, instance, **kwargs):
    # Skip if profile_image is empty or the default
    if (instance.profile_image and instance.profile_image.name and 
        instance.profile_image.name != instance.profile_image.field.default):
        if default_storage.exists(instance.profile_image.name):
            default_storage.delete(instance.profile_image.name)
            
#ORGANIZATION
@receiver(pre_save, sender=organization)
def delete_old_organization_logo(sender, instance, **kwargs):
    if not instance.pk:  # If this is a new instance, skip
        return
    
    try:
        old_instance = organization.objects.only('logo').get(pk=instance.pk)
    except organization.DoesNotExist:
        return
    
    # Skip if old logo is empty, None, or the default
    if (old_instance.logo and old_instance.logo.name and 
        instance.logo != old_instance.logo and  # Check if the logo has changed
        old_instance.logo.name != old_instance.logo.field.default and 
        default_storage.exists(old_instance.logo.name)):
        default_storage.delete(old_instance.logo.name)

# Optional: Add post_delete signal to clean up logo when an Organization is deleted
@receiver(post_delete, sender=organization)
def delete_organization_logo(sender, instance, **kwargs):
    # Skip if logo is empty or the default
    if (instance.logo and instance.logo.name and 
        instance.logo.name != instance.logo.field.default):
        if default_storage.exists(instance.logo.name):
            default_storage.delete(instance.logo.name)