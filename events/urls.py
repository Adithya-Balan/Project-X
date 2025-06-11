from django.urls import path
from . import views

urlpatterns = [
    path("event/<int:id>/", views.event_detail, name = 'event_detail'),
    path("event-form/<int:id>/", views.org_event_form, name="org_event_form"),
    path("event-form-edit/<int:org_id>/<int:event_id>/", views.event_form_edit, name="event_form_edit"),
    
    path("toggle_event_save/<int:eventId>/", views.toggle_event_save, name="toggle_event_save"),
    path("toggle_comment_like/<int:comment_id>/", views.toggle_like_comment, name="toggle_comment_like"),
    path("toggle_reply_like/<int:reply_id>/", views.toggle_like_reply, name="toggle_reply_like"),
    path('save-comment/<int:event_id>/', views.save_event_comment, name='save_event_comment'),
    path('save-reply/', views.save_event_reply, name='save_event_reply'),   
    path("delete-event/<uuid:uuid>/", views.delete_event, name="delete_event"),
]
