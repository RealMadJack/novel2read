from django.shortcuts import render, redirect
from django.views.generic import View, DetailView, ListView

from .models import Book


class FrontPageView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, template_name='books/front_page.html', context=context)


class GenrePageView(ListView):
    # model = Book
    template_name = 'books/genre.html'
    # paginate_by = 20

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['books'] = Book.objects.all()
    #     return context

    def get(self, request, *args, **kwargs):
        try:
            books = Book.objects.select_related('bookgenre').prefetch_related('booktag')
            if kwargs:
                print(f'kwargs: {kwargs}')
                books = Book.objects.filter(bookgenre__slug=kwargs['bookgenre_slug'])
                print(books)
            context = {'books': books}
            return render(request, template_name=self.template_name, context=context)
        except Book.DoesNotExist:
            return redirect('/404/')


class BookView(DetailView):
    pass
