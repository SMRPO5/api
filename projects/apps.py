from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    name = 'projects'

    def ready(self):
        from .signals import handlers