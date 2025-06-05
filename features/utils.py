from myapp.models import userinfo
from .models import TrendingLeaderboard
from datetime import datetime, timedelta
import pytz
from django.db.models import F
from django.db.models.functions import Greatest
from django.core.exceptions import ObjectDoesNotExist

def get_week_range():
    # Get the current week's start and end (Monday 00:00 to Sunday 23:59:59 IST)
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    days_since_monday = now.weekday()
    week_start = now - timedelta(days=days_since_monday)
    week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
    week_end = week_start + timedelta(days=6, hours=23, minutes=59, seconds=59)
    return week_start, week_end

def update_leaderboard_entry(user_info, post=False, project=False, action=False, 
                            remove_post=False, remove_project=False, remove_action=False):
    # Check if user_info exists in the database
    try:
        userinfo.objects.get(pk=user_info.pk)
    except ObjectDoesNotExist:
        return  # Skip if user_info has been deleted
    
    current_week_start = TrendingLeaderboard.get_current_week_start()
    
    leaderboard, created = TrendingLeaderboard.objects.get_or_create(
        user=user_info,
        defaults={'week_start': current_week_start}
    )

    # Reset counts if the week has changed or it's a new entry
    if created or leaderboard.week_start < current_week_start:
        leaderboard.posts_count = 0
        leaderboard.projects_count = 0
        leaderboard.actions_count = 0
        leaderboard.score = 0
        leaderboard.week_start = current_week_start
        leaderboard.save()

    # Atomically increment or decrement counts
    update_needed = False
    if post:
        leaderboard.posts_count = F('posts_count') + 1
        update_needed = True
    if project:
        leaderboard.projects_count = F('projects_count') + 1
        update_needed = True
    if action:
        leaderboard.actions_count = F('actions_count') + 1
        update_needed = True
    if remove_post:
        leaderboard.posts_count = Greatest(F('posts_count') - 1, 0)  # Ensure not below 0
        update_needed = True
    if remove_project:
        leaderboard.projects_count = Greatest(F('projects_count') - 1, 0)  # Ensure not below 0
        update_needed = True
    if remove_action:
        leaderboard.actions_count = Greatest(F('actions_count') - 1, 0)  # Ensure not below 0
        update_needed = True

    if update_needed:
        leaderboard.save()  # Save the F expressions
        leaderboard.refresh_from_db()  # Get the updated values
        leaderboard.score = leaderboard.calculate_score()
        leaderboard.save()  # Save the updated score

def reset_all_leaderboard_entries():
    # Reset all leaderboard entries at the beginning of the week
    current_week_start = TrendingLeaderboard.get_current_week_start()
    TrendingLeaderboard.objects.update(
        posts_count=0,
        projects_count=0,
        actions_count=0,
        score=0,
        week_start=current_week_start
    )