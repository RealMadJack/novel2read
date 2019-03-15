from django.shortcuts import render, redirect
from django.views.generic import View, DetailView, ListView

from .models import Book, BookTag


class FrontPageView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, template_name='books/front_page.html', context=context)


class BookGenreView(ListView):
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
                books = Book.objects.filter(bookgenre__slug=kwargs['bookgenre_slug'])
            context = {'books': books}
            return render(request, template_name=self.template_name, context=context)
        except Book.DoesNotExist:
            return redirect('/404/')


class BookTagView(ListView):
    template_name = 'books/tag.html'

    def get(self, request, *args, **kwargs):
        try:
            tags = BookTag.objects.all()
            context = {'tags': tags}
            if kwargs:
                tag = BookTag.objects.prefetch_related('books').get(slug=kwargs['booktag_slug'])
                books = Book.objects.filter(booktag__slug=kwargs['booktag_slug'])
                context['tag'] = tag
                context['books'] = books
            return render(request, template_name=self.template_name, context=context)
        except BookTag.DoesNotExist:
            return redirect('/404/')


class BookView(DetailView):
    template_name = 'books/book.html'

    def get(self, request, *args, **kwargs):
        try:
            books = Book.objects.select_related('bookgenre').prefetch_related('booktag')
            book = Book.objects.get(slug=kwargs['book_slug'])
            context = {'books': books, 'book': book}
            return render(request, template_name=self.template_name, context=context)
        except Book.DoesNotExist:
            return redirect('/404/')


class BookChapterView(DetailView):
    template_name = 'books/chapter.html'

    def get(self, request, *args, **kwargs):
        pass
