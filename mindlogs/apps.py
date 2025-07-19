from django.apps import AppConfig


class MindlogsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mindlogs'
    
    def ready(self):
        import mindlogs.signals
