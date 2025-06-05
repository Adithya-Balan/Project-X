from django.db.models.signals import post_save, m2m_changed, post_delete
from django.dispatch import receiver
from myapp.models import post, projects, post_comments, userinfo
from .utils import update_leaderboard_entry
from django.core.exceptions import ObjectDoesNotExist
from django.db.transaction import on_commit

# Helper function to delay leaderboard updates
def delay_leaderboard_update(func, *args, **kwargs):
    def wrapped():
        try:
            func(*args, **kwargs)
        except ObjectDoesNotExist:
            pass  # Skip if user_info has been deleted
    on_commit(wrapped)

# Signal for when a new post is created
@receiver(post_save, sender=post)
def update_on_post_save(sender, instance, created, **kwargs):
    if created:
        try:
            user_info = instance.user
            if user_info:
                delay_leaderboard_update(
                    update_leaderboard_entry,
                    user_info=user_info,
                    post=True
                )
        except ObjectDoesNotExist:
            pass  # Skip if user_info doesn't exist

# Signal for when a post is deleted
@receiver(post_delete, sender=post)
def update_on_post_delete(sender, instance, **kwargs):
    try:
        user_info = instance.user
        if user_info:
            delay_leaderboard_update(
                update_leaderboard_entry,
                user_info=user_info,
                remove_post=True
            )
    except ObjectDoesNotExist:
        pass  # Skip if user_info doesn't exist

# Signal for when a new project is created
@receiver(post_save, sender=projects)
def update_on_project_save(sender, instance, created, **kwargs):
    if created:
        try:
            user_info = instance.creator
            if user_info:
                delay_leaderboard_update(
                    update_leaderboard_entry,
                    user_info=user_info,
                    project=True
                )
        except ObjectDoesNotExist:
            pass

# Signal for when a project is deleted
@receiver(post_delete, sender=projects)
def update_on_project_delete(sender, instance, **kwargs):
    try:
        user_info = instance.creator
        if user_info:
            delay_leaderboard_update(
                update_leaderboard_entry,
                user_info=user_info,
                remove_project=True
            )
    except ObjectDoesNotExist:
        pass

# Signal for when a user joins or leaves a project
@receiver(m2m_changed, sender=projects.members.through)
def update_on_project_join(sender, instance, action, pk_set, **kwargs):
    try:
        creator = instance.creator  # Cache creator to avoid repeated access
    except ObjectDoesNotExist:
        return  # Skip if creator doesn't exist
    if action == "post_add":
        for user_pk in pk_set:
            try:
                user_info = userinfo.objects.get(pk=user_pk)
                if user_info != creator:  # Don't count the creator
                    delay_leaderboard_update(
                        update_leaderboard_entry,
                        user_info=user_info,
                        action=True
                    )
            except ObjectDoesNotExist:
                pass
    elif action == "post_remove":
        for user_pk in pk_set:
            try:
                user_info = userinfo.objects.get(pk=user_pk)
                if user_info != creator:  # Don't count the creator
                    delay_leaderboard_update(
                        update_leaderboard_entry,
                        user_info=user_info,
                        remove_action=True
                    )
            except ObjectDoesNotExist:
                pass

# Signal for when a new comment is created
@receiver(post_save, sender=post_comments)
def update_on_comment_save(sender, instance, created, **kwargs):
    if created:
        try:
            user_info = instance.user
            if user_info:
                delay_leaderboard_update(
                    update_leaderboard_entry,
                    user_info=user_info,
                    action=True
                )
        except ObjectDoesNotExist:
            pass

# Signal for when a comment is deleted
@receiver(post_delete, sender=post_comments)
def update_on_comment_delete(sender, instance, **kwargs):
    try:
        user_info = instance.user
        if user_info:
            delay_leaderboard_update(
                update_leaderboard_entry,
                user_info=user_info,
                remove_action=True
            )
    except ObjectDoesNotExist:
        pass

# Signal for when a user likes or unlikes a post
@receiver(m2m_changed, sender=post.likes.through)
def update_on_like(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        for user_pk in pk_set:
            try:
                user_info = userinfo.objects.get(pk=user_pk)
                delay_leaderboard_update(
                    update_leaderboard_entry,
                    user_info=user_info,
                    action=True
                )
            except ObjectDoesNotExist:
                pass
    elif action == "post_remove":
        for user_pk in pk_set:
            try:
                user_info = userinfo.objects.get(pk=user_pk)
                delay_leaderboard_update(
                    update_leaderboard_entry,
                    user_info=user_info,
                    remove_action=True
                )
            except ObjectDoesNotExist:
                pass