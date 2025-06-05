from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrendingLeaderboardViewSet

router = DefaultRouter()
router.register(r'trending-leaderboard', TrendingLeaderboardViewSet)

urlpatterns = [
    path('', include(router.urls)),
]