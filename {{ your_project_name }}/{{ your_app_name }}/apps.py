from django.apps import AppConfig


class TemplateAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = '{{ your_app_name }}'
