from django.urls import path
from . import views

urlpatterns = [
    path("project/<int:id>/", views.project_detail, name="project_detail"),
    path("project/<int:id>/members/", views.project_joined_members, name="project_joined_members"),
    path("project-form/<uuid:uuid>/", views.project_form_edit, name="project_form"), #For Existing Project
    path('project-form/', views.project_form, name='project_form_new'),   # For creating new project
    
    # Project joining
    path("request-project-join/<int:project_id>/", views.toggle_project_request, name="toggle_project_request"),
    path("leave-project-members/<int:project_id>/", views.leave_project_members, name="leave_project_Members"),
    path("accept-or-reject-request/<int:project_id>/<int:user_id>/", views.handle_project_request_creator, name='handle_project_request_creator'),
    
    #Others ajax req
    path("toggle_project_save/<int:project_id>/", views.toggle_project_save, name="toggle_project_save"),
    path("toggle_comment_like/<int:comment_id>/", views.toggle_like_project_comment, name="toggle_comment_like"),
    path("toggle_reply_like/<int:reply_id>/", views.toggle_like_reply, name="toggle_reply_like"),
    path('save-comment/<int:project_id>/', views.save_project_comment, name='save_project_comment'),
    path('save-reply/', views.save_project_reply, name='save_project_reply'),   
    
    path("delete-project/<uuid:uuid>/", views.delete_project, name="delete_project"),
]
