from django.db import models


class BookManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=1)

    # def published(self):
    #     return self.filter(status=1)
