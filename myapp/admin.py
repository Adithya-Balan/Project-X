from django.contrib import admin
from .models import organization, skill, userinfo, education, current_position, experience, follow, projects, Domain,  user_project, project_comment, project_reply, user_status, SavedItem, post, post_comments, event, Notification, Industry, CringeBadge
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from features.models import TrendingLeaderboard
from mindlogs.models import MindLog

# Register your models here.
admin.site.register(skill)
admin.site.register(organization)
admin.site.register(education)
admin.site.register(current_position)
admin.site.register(experience)
admin.site.register(follow)
admin.site.register(Domain)
admin.site.register(user_project)
admin.site.register(project_comment)
admin.site.register(project_reply)
admin.site.register(user_status)
admin.site.register(SavedItem)
admin.site.register(post)
admin.site.register(post_comments)
admin.site.register(Notification)
admin.site.register(Industry)
admin.site.register(CringeBadge)
admin.site.register(TrendingLeaderboard)

@admin.register(userinfo)
class userinfoAdmin(admin.ModelAdmin):
    # Show UUID as read-only in the detail/edit page
    readonly_fields = ('uuid',)

@admin.register(projects)
class projectsAdmin(admin.ModelAdmin):
    # Show UUID as read-only in the detail/edit page
    readonly_fields = ('uuid',)
    
@admin.register(event)
class eventAdmin(admin.ModelAdmin):
    # Show UUID as read-only in the detail/edit page
    readonly_fields = ('uuid',)
    
@admin.register(MindLog)
class MindLogAdmin(admin.ModelAdmin):
    readonly_fields = ('sig',)
    
class CustomUserAdmin(UserAdmin):
    ordering = ['-date_joined']

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)