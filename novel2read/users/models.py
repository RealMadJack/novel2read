from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.db.models import CharField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from novel2read.apps.books.models import Book


class User(AbstractUser):
    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = CharField(_("Name of User"), blank=True, max_length=255)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profile data')


class Library(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ManyToManyField(Book, related_name='%(class)ss', blank=True)

    class Meta:
        verbose_name = _('Library')
        verbose_name_plural = _('Library data')


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile_library(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Library.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile_library(sender, instance, **kwargs):
    instance.profile.save()
    instance.library.save()
