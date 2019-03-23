from django.shortcuts import render, redirect
from django.views.generic import View, DetailView, ListView

from next_prev import next_in_order, prev_in_order
from .models import Book, BookTag, BookChapter


class FrontPageView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, template_name='books/front_page.html', context=context)


class BookGenreView(ListView):
    template_name = 'books/bookgenre.html'

    def get(self, request, *args, **kwargs):
        try:
            books = Book.objects.select_related('bookgenre').prefetch_related('booktag').filter(status=1)
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
                books = tag.books.select_related('bookgenre').prefetch_related('booktag').filter(status=1)
                context['tag'] = tag
                context['books'] = books
            return render(request, template_name=self.template_name, context=context)
        except BookTag.DoesNotExist:
            return redirect('/404/')


class BookView(DetailView):
    template_name = 'books/book.html'

    def get(self, request, *args, **kwargs):
        try:
            books = Book.objects.select_related('bookgenre').prefetch_related('booktag', 'bookchapters').filter(status=1)
            book = books.get(slug=kwargs['book_slug'])
            last_chap = book.bookchapters.last()
            context = {'books': books, 'book': book, 'last_chap': last_chap}
            if request.user.is_authenticated:
                book_in = book in request.user.library.book.all()
                context['book_in'] = book_in
            return render(request, template_name=self.template_name, context=context)
        except Book.DoesNotExist:
            return redirect('/404/')


class BookChapterView(DetailView):
    template_name = 'books/bookchapter.html'

    def get(self, request, *args, **kwargs):
        try:
            bookchapter = BookChapter.objects.select_related('book').get(c_id=kwargs['c_id'])
            bookchapters = BookChapter.objects.filter(book__slug=kwargs['book_slug']).select_related('book')
            prev_chap = prev_in_order(bookchapter, qs=bookchapters)
            next_chap = next_in_order(bookchapter, qs=bookchapters)
            context = {
                'bookchapters': bookchapters,
                'bookchapter': bookchapter,
                'prev_chap': prev_chap, 'next_chap': next_chap}
            if request.user.is_authenticated:
                from novel2read.apps.users.models import BookProgress
                try:
                    book_prog = BookProgress.objects.get(book=bookchapter.book)
                    book_prog.c_id = bookchapter.c_id
                    book_prog.save()
                except BookProgress.DoesNotExist:
                    BookProgress.objects.create(
                        book=bookchapter.book,
                        library=request.user.library,
                        c_id=bookchapter.c_id,
                    )

            return render(request, template_name=self.template_name, context=context)
        except (Book.DoesNotExist, BookChapter.DoesNotExist):
            return redirect('/404/')
