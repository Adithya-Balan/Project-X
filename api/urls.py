from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'trending-leaderboard', views.TrendingLeaderboardViewSet)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('', include(router.urls)),
    
    path('launch-chat/', views.launch_chat_for_loggedin_user, name='launch_chat_for_logggedin_user'),
    path('chat/user/<int:userinfo_id>/', views.get_chat_userprofile), #Get any userinfo using id
    path("chat/users/info/", views.get_usersinfo, name='get_usersinfo')
]