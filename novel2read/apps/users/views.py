from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView, RedirectView, UpdateView

from novel2read.apps.books.models import Book

User = get_user_model()


@login_required
def library_view(request, *args, **kwargs):
    if request.method == 'GET':
        template_name = 'users/user_library.html'
        books = request.user.library.book.select_related('bookprogress').all()
        context = {'books': books}
        return render(request, template_name=template_name, context=context)


@login_required
def add_remove_library_book_ajax(request, *args, **kwargs):
    data = {'is_valid': False}

    if request.is_ajax():
        data['is_valid'] = True
        data['in_lib'] = True
        user = request.user
        book = Book.objects.get(slug=kwargs['book_slug'])
        user.library.book.add(book)
        user.save()

    return JsonResponse(data)


@login_required
def add_library_book(request, *args, **kwargs):
    if request.method == 'POST':
        try:
            book = Book.objects.get(slug=kwargs['book_slug'])
            user = User.objects.get(id=request.user.id)
            next_url = request.POST.get('next', reverse('users:library', kwargs={'username': user.username}))
            if user is not None:
                user.library.book.add(book)
                user.save()
                return redirect(next_url)
            return redirect('/403/')
        except (Book.DoesNotExist, User.DoesNotExist):
            return redirect('/403/')
    return redirect('/400/')


@login_required
def remove_library_book(request, *args, **kwargs):
    if request.method == 'POST':
        try:
            book = Book.objects.get(slug=kwargs['book_slug'])
            user = User.objects.get(id=request.user.id)
            next_url = request.POST.get('next', reverse('users:library', kwargs={'username': user.username}))
            if user is not None:
                user.library.book.remove(book)
                user.save()
                return redirect(next_url)
            return redirect('/403/')
        except (Book.DoesNotExist, User.DoesNotExist):
            return redirect('/403/')
    return redirect('/400/')


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
