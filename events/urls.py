from django.urls import path
from . import views

urlpatterns = [
    path("toggle_comment_like/<int:comment_id>/", views.toggle_like_comment, name="toggle_comment_like"),
    path("toggle_reply_like/<int:reply_id>/", views.toggle_like_reply, name="toggle_reply_like"),
    path('save-comment/<int:event_id>/', views.save_event_comment, name='save_event_comment'),
    path('save-reply/', views.save_event_reply, name='save_event_reply'),   
]
