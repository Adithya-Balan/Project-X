from django.urls import path
from . import views

urlpatterns = [
    path("toggle_comment_like/<int:comment_id>/", views.toggle_like_project_comment, name="toggle_comment_like"),
    path("toggle_reply_like/<int:reply_id>/", views.toggle_like_reply, name="toggle_reply_like"),
    path('save-comment/<int:project_id>/', views.save_project_comment, name='save_project_comment'),
    path('save-reply/', views.save_project_reply, name='save_project_reply'),   
]
