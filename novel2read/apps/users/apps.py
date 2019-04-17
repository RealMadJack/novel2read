from django.apps import AppConfig


class UsersAppConfig(AppConfig):

    name = "novel2read.apps.users"
    verbose_name = "Users"

    def ready(self):
        try:
            import novel2read.apps.users.signals  # noqa F401
        except ImportError:
            pass
