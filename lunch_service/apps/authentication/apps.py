from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lunch_service.apps.authentication'
    verbose_name = 'Authentication'

    def ready(self):
        import lunch_service.apps.authentication.signals  