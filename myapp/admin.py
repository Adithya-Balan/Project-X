from django.contrib import admin
from .models import organization, skill, userinfo, education, current_position, experience, follow, projects, Domain,  user_project, project_comment, project_reply

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