from django.http import HttpResponseRedirect, HttpResponseServerError, JsonResponse
from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.decorators import login_required
from features.models import TrendingLeaderboard
from features.utils import reset_all_leaderboard_entries
from rest_framework_simplejwt.exceptions import TokenError
from .serializers import TrendingLeaderboardSerializer
import logging
import requests

from myapp.models import userinfo

logger = logging.getLogger(__name__)

@login_required
def launch_chat_for_loggedin_user(request):
    user = request.user
    info = user.info
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    payload = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "userinfo_id": info.id,
        "username": user.username,
        "profile_image": request.build_absolute_uri(info.profile_image.url) if info.profile_image else None,
    }

    try:
        # POST to your chat backend
        res = requests.post("http://base-chat-url/api/user/initialize_token", json=payload)
        print(res.status_code)
        # redirect to React frontend
        if res.status_code == 200:
            return redirect("http://base-chat-url:3000")
        else:
            return redirect("http://base-chat-url:3000/error")
    except Exception as e:
        return redirect("http:// base-chat-url:3000/error")

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
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chat_userprofile(request, userinfo_id):
    try:
        userinfo_obj = userinfo.objects.get(id=userinfo_id)
        return Response({
            "userinfo_id": userinfo_obj.id,
            "username": userinfo_obj.user.username,
            "profile_image": request.build_absolute_uri(userinfo_obj.profile_image.url) if userinfo_obj.profile_image else None
        })
    except userinfo.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_usersinfo(request):
    ids = request.data.get("user_ids", [])
    users = userinfo.objects.filter(id__in=ids)
    
    data = [
        {
            "userinfo_id": u.id,
            "username": u.user.username,
            "profile_image": request.build_absolute_uri(u.profile_image.url) if u.profile_image else None
        }
        for u in users
    ]
    return Response(data)