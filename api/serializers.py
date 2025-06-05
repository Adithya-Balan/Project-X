from rest_framework import serializers
from features.models import TrendingLeaderboard

class TrendingLeaderboardSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.user.username')
    profile_image = serializers.ImageField(source='user.profile_image')
    
    class Meta:
        model = TrendingLeaderboard
        fields = ['username', 'profile_image', 'score', 'posts_count', 'projects_count', 'actions_count', 'last_updated']