from django.db import models
from django_comments_xtd.models import XtdComment


class BasicComment(XtdComment):
    user_avatar = models.CharField(blank=True, max_length=255)
