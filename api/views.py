from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from features.models import TrendingLeaderboard
from features.utils import reset_all_leaderboard_entries
from .serializers import TrendingLeaderboardSerializer
import logging

logger = logging.getLogger(__name__)

class TrendingLeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TrendingLeaderboard.objects.all()[:25]  # Top 25 users
    serializer_class = TrendingLeaderboardSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        logger.info(f"Trending leaderboard accessed by user: {request.user.username}")
        # Check if a reset is needed (in case the command wasn't run)
        current_week_start = TrendingLeaderboard.get_current_week_start()
        if TrendingLeaderboard.objects.filter(week_start__lt=current_week_start).exists():
            reset_all_leaderboard_entries()
        # Get the top 25 users
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
