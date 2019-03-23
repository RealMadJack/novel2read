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


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile_library(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Library.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile_library(sender, instance, **kwargs):
    instance.profile.save()
    instance.library.save()


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.URLField(_('User Image'), blank=True, default='https://cdn2.iconfinder.com/data/icons/user-profile/100/User-512.png', max_length=255)
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

    def __str__(self):
        return self.user.username


class BookProgress(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE)
    library = models.ForeignKey(Library, on_delete=models.SET_NULL, blank=True, null=True)
    # bc_id = models.IntegerField('Chapter ID', blank=True, null=True, default=0)
    c_id = models.IntegerField('Chapter ID', blank=True, null=True, default=0)
    # scroll position

    class Meta:
        verbose_name = 'Book Progress'
        verbose_name_plural = 'Book Progresses'

    def __str__(self):
        return f'{self.library}: {self.book.title} Chapter {self.c_id}'