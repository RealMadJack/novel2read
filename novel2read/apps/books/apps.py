from django.apps import AppConfig


class BooksConfig(AppConfig):
    name = 'novel2read.apps.books'
    verbose_name = "books"

    def ready(self):
        try:
            import novel2read.apps.books.signals  # noqa F401
        except ImportError:
            pass
