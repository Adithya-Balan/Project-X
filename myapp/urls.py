from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path("sign-up", views.sign_up.as_view(), name="sign_up"),
    path("home", views.index, name="index"),
    path("edit-profile", views.edit_profile, name="edit_profile"),
    
    path("explore-dev", views.explore_dev, name="explore_dev"),
    path("explore-projects", views.explore_project, name="explore-project"),
    path("explore-organization", views.explore_organization, name="explore_organization"),
    path("explore-events", views.explore_events, name="explore_events"),
    
    path("project/<int:id>", views.project_detail, name="project_detail"),
    path("project/<int:id>/members", views.project_detail_members, name="project_detail_members"),
    path("project/<int:id>/forum", views.project_forum, name="project_forum"),
    path("join-project/<int:id>/", views.join_project, name="join_project"),
    
    path("create-org", views.create_organization, name="create_organiation"),
    path("organization/<int:id>", views.organization_detail, name="organization_detail"),
    path("<int:org_id>/follow-list", views.org_follow_list, name="org_follow_list"),
    path('organization/<int:organization_id>/follow/', views.follow_organization, name='follow_organization'),
    path('organization/<int:organization_id>/unfollow/', views.unfollow_organization, name='unfollow_organization'),
    path("event-form/<int:id>", views.org_event_form, name="org_event_form"),
    path("event-form-edit/<int:org_id>/<int:event_id>", views.event_form_edit, name="event_form_edit"),
    
    path("event/<int:id>", views.event_detail, name = 'event_detail'),
    path("event/<int:id>/forum", views.event_forum, name="event_forum"),
    
    # User-profile
    path("user-profile/<str:user_name>", views.user_profile, name="user_profile"),
    path("<str:username>/follow-list", views.follow_list, name="follow_list"),
    path("unfollow/<int:otheruserinfo_id>/", views.unfollow_user, name = 'unfollow_user'),
    path("follow/<int:otheruserinfo_id>/", views.follow_user, name = 'follow_user'),
    path('saved', views.saved_page, name = 'saved_page'),
    
    path("toggle_project_save/<int:project_id>/", views.toggle_project_save, name="toggle_project_save"),
    path("toggle_event_save/<int:eventId>/", views.toggle_event_save, name="toggle_event_save"),
    path('toggle_like/<int:post_id>/', views.toggle_like, name = 'toggle_like'),
    path("toggle_post_save/<int:post_id>/", views.toggle_post_save, name="toggle_post_save"),
    path("save-post", views.save_post, name="save_post"),
    path("save-comment/", views.save_comment, name="save_comment"),
    path('delete-post-comment/<int:comment_id>/', views.delete_post_comment, name='delete_post_comment'),
    
    path("calendar", views.calendar_page, name="calendar_page"),
    path("settings", views.settings_page, name="settings_page"),
    path('delete-data', views.delete_data, name = 'delete_data')
]
