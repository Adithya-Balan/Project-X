from django.core.management.base import BaseCommand
from features.utils import reset_all_leaderboard_entries

class Command(BaseCommand):
    help = 'Resets the trending leaderboard at the beginning of the week'

    def handle(self, *args, **kwargs):
        reset_all_leaderboard_entries()
        self.stdout.write(self.style.SUCCESS('Successfully reset leaderboard'))