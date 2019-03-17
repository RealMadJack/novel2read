from django.shortcuts import render, redirect
from django.views.generic import View, DetailView, ListView

from next_prev import next_in_order, prev_in_order
from .models import Book, BookTag, BookChapter


class FrontPageView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, template_name='books/front_page.html', context=context)


class BookGenreView(ListView):
    # model = Book
    template_name = 'books/bookgenre.html'
    # paginate_by = 20

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['books'] = Book.objects.all()
    #     return context

    def get(self, request, *args, **kwargs):
        try:
            books = Book.objects.select_related('bookgenre').prefetch_related('booktag')
            if kwargs:
                books = books.filter(bookgenre__slug=kwargs['bookgenre_slug'])
            context = {'books': books}
            return render(request, template_name=self.template_name, context=context)
        except Book.DoesNotExist:
            return redirect('/404/')


class BookTagView(ListView):
    template_name = 'books/booktag.html'

    def get(self, request, *args, **kwargs):
        try:
            tags = BookTag.objects.all()
            context = {'tags': tags}
            if kwargs:
                tag = tags.get(slug=kwargs['booktag_slug'])
                books = Book.objects.select_related('bookgenre').prefetch_related('booktag')
                books = books.filter(booktag__slug=kwargs['booktag_slug'])
                context['tag'] = tag
                context['books'] = books
            return render(request, template_name=self.template_name, context=context)
        except BookTag.DoesNotExist:
            return redirect('/404/')


class BookView(DetailView):
    template_name = 'books/book.html'

    def get(self, request, *args, **kwargs):
        try:
            books = Book.objects.select_related('bookgenre').prefetch_related('booktag', 'bookchapters')
            book = books.get(slug=kwargs['book_slug'])
            context = {'books': books, 'book': book}
            return render(request, template_name=self.template_name, context=context)
        except Book.DoesNotExist:
            return redirect('/404/')


class BookChapterView(DetailView):
    template_name = 'books/bookchapter.html'

    def get(self, request, *args, **kwargs):
        try:
            bookchapter = BookChapter.objects.get(pk=kwargs['bookchapter_pk'])
            bookchapters = BookChapter.objects.filter(book__slug=kwargs['book_slug']).select_related('book')
            prev_chap = prev_in_order(bookchapter, qs=bookchapters)
            next_chap = next_in_order(bookchapter, qs=bookchapters)
            context = {
                'bookchapters': bookchapters,
                'bookchapter': bookchapter,
                'prev_chap': prev_chap, 'next_chap': next_chap}
            return render(request, template_name=self.template_name, context=context)
        except (Book.DoesNotExist, BookChapter.DoesNotExist):
            return redirect('/404/')
