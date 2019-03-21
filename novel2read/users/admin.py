from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from novel2read.users.forms import UserChangeForm, UserCreationForm
from .models import Profile, Library

User = get_user_model()


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class LibraryInline(admin.StackedInline):
    model = Library
    filter_horizontal = ('book', )
    can_delete = False


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    inlines = (ProfileInline, LibraryInline, )
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("name",)}),) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]
