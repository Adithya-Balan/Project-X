from django.db import models
from myapp.models import userinfo
from datetime import datetime, timedelta
import pytz

class TrendingLeaderboard(models.Model):
    user = models.OneToOneField(userinfo, on_delete=models.CASCADE, related_name='trending_leaderboard')
    score = models.IntegerField(default=0, db_index=True)  # Total activity score
    posts_count = models.IntegerField(default=0)  # Number of posts in the week
    projects_count = models.IntegerField(default=0)  # Number of projects created in the week
    actions_count = models.IntegerField(default=0)  # Number of actions in the week
    week_start = models.DateTimeField()  # Start of the week for this data
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-score', 'user__user__username']  # Sort by score (desc), then username (asc)
        indexes = [
            models.Index(fields=['week_start']),  # Index for faster reset queries
        ]

    def __str__(self):
        return f"{self.id} {self.user.user.username}: {self.score} points (Week starting {self.week_start})"

    @staticmethod
    def get_current_week_start():
        # Get the start of the current week (Monday 00:00 IST)
        ist = pytz.timezone('Asia/Kolkata')
        now = datetime.now(ist)
        days_since_monday = now.weekday()
        week_start = now - timedelta(days=days_since_monday)
        week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
        return week_start

    def calculate_score(self):
        # Total Activity Score = (Posts × 3) + (Projects × 5) + (Actions × 1)
        return (self.posts_count * 3) + (self.projects_count * 5) + (self.actions_count * 1)