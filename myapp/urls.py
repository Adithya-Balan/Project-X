from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path("sign-up", views.sign_up.as_view(), name="sign_up"),
    path("home", views.index, name="index"),
    
    path("explore-dev", views.explore_dev, name="explore_dev"),
    path("explore-projects", views.explore_project, name="explore-project"),
    path("project/<int:id>", views.project_detail, name="project_detail"),
    path("project/<int:id>/forum", views.project_forum, name="project_forum"),
    path("join-project/<int:id>/", views.join_project, name="join_project"),
    
    # User-profile
    path("user-profile/<str:username>", views.user_profile, name="user_profile"),
    path("<str:username>/follow-list", views.follow_list, name="follow_list"),
    path("unfollow/<int:otheruserinfo_id>", views.unfollow_user, name = 'unfollow_user'),
    path("follow/<int:otheruserinfo_id>", views.follow_user, name = 'follow_user'),
        
]
