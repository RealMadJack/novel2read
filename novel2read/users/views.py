from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView, RedirectView, UpdateView

from novel2read.apps.books.models import Book

User = get_user_model()


@login_required
def library_view(request, *args, **kwargs):
    pass


@login_required
def add_library_book(request, *args, **kwargs):
    if request.method == 'POST':
        try:
            book = Book.objects.get(slug=kwargs['book_slug'])
            user = User.library.book.add()
            user.save()
            return redirect(reverse('books:book', kwargs={'book_slug': kwargs['book_slug']}))
        except Book.DoesNotExist:
            return redirect('/404/')
    return redirect(reverse('users:library-add', kwargs={'book_slug': kwargs['book_slug']}))


@login_required
def remove_library_book(request, *args, **kwargs):
    if request.method == 'POST':
        pass
    return redirect(reverse('users:library'))


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserListView(LoginRequiredMixin, ListView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_list_view = UserListView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    fields = ["name"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()
