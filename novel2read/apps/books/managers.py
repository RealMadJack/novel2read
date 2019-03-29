from django.db import models


class BookManager(models.Manager):
    def published(self):
        return self.filter(status=1)
