from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from novel2read.apps.users.forms import UserChangeForm, UserCreationForm
from novel2read.apps.users.models import Profile, Library, BookProgress

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
    list_select_related = ('library__user', 'profile__user')
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]


@admin.register(BookProgress)
class BookProgress(admin.ModelAdmin):
    fields = ('library', 'book', 'c_id', )
    list_select_related = ('book', 'library__user')
    list_display = ('library', 'book', 'c_id')