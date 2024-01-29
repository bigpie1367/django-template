from django.apps import AppConfig


class TemplateAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = '{{ your_project_name }}_site'
