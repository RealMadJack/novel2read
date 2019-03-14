from django.shortcuts import render
from django.views.generic import View, ListView

from .models import Book


class FrontPageView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, template_name='books/front_page.html', context=context)


class GenrePageView(ListView):
    # request book=>booktag select, global bookgenre
    model = Book
    template_name = 'books/genre.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.all()
        return context
