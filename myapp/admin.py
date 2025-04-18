from django.contrib import admin
from .models import organization, skill, userinfo, education, current_position, experience, follow, projects, Domain,  user_project, project_comment, project_reply, user_status, SavedItem, post, post_comments, event, Notification, Industry, CringeBadge

# Register your models here.
admin.site.register(skill)
admin.site.register(userinfo)
admin.site.register(organization)
admin.site.register(education)
admin.site.register(current_position)
admin.site.register(experience)
admin.site.register(projects)
admin.site.register(follow)
admin.site.register(Domain)
admin.site.register(user_project)
admin.site.register(project_comment)
admin.site.register(project_reply)
admin.site.register(user_status)
admin.site.register(SavedItem)
admin.site.register(post)
admin.site.register(post_comments)
admin.site.register(event)
admin.site.register(Notification)
admin.site.register(Industry)
admin.site.register(CringeBadge)