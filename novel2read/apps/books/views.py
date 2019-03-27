from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View, DetailView, ListView

from next_prev import next_in_order, prev_in_order
from .models import Book, BookTag, BookChapter
from .forms import BookSearchForm
from novel2read.apps.users.models import BookProgress


class FrontPageView(View):
    def get(self, request, *args, **kwargs):
        books = Book.objects.prefetch_related('bookchapters').filter(status=1)
        context = {'books': books}
        return render(request, template_name='books/front_page.html', context=context)


class BookGenreView(ListView):
    template_name = 'books/bookgenre.html'

    def get(self, request, *args, **kwargs):
        try:
            books = Book.objects.select_related('bookgenre').prefetch_related('booktag').filter(status=1).order_by('-votes')
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
                books = tag.books.select_related('bookgenre').prefetch_related('booktag').filter(status=1).order_by('-votes')
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
            first_chap = book.bookchapters.first()
            last_chap = book.bookchapters.last()
            user_auth = request.user.is_authenticated
            context = {
                'books': books, 'book': book,
                'first_chap': first_chap, 'last_chap': last_chap,
                'user_auth': user_auth}
            if user_auth:
                book_prog = False
                context['user_lib'] = list(request.user.library.book.all())
                try:
                    book_prog = BookProgress.objects.get(user=request.user, book=book)
                    context['book_prog'] = book_prog
                except BookProgress.DoesNotExist:
                    context['book_prog'] = book_prog
            return render(request, template_name=self.template_name, context=context)
        except Book.DoesNotExist:
            return redirect('/404/')


class BookChapterView(DetailView):
    template_name = 'books/bookchapter.html'

    def get(self, request, *args, **kwargs):
        try:
            bookchapter = BookChapter.objects.select_related('book').get(book__slug=kwargs['book_slug'], c_id=kwargs['c_id'],)
            bookchapters = BookChapter.objects.filter(book__slug=kwargs['book_slug']).select_related('book')
            prev_chap = prev_in_order(bookchapter, qs=bookchapters)
            next_chap = next_in_order(bookchapter, qs=bookchapters)
            context = {
                'bookchapters': bookchapters,
                'bookchapter': bookchapter,
                'prev_chap': prev_chap, 'next_chap': next_chap}
            if request.user.is_authenticated:
                try:
                    book_prog = BookProgress.objects.get(user=request.user, book=bookchapter.book)
                    book_prog.c_id = bookchapter.c_id
                    book_prog.save()
                except BookProgress.DoesNotExist:
                    BookProgress.objects.create(
                        book=bookchapter.book,
                        user=request.user,
                        c_id=bookchapter.c_id,
                    )
            return render(request, template_name=self.template_name, context=context)
        except (Book.DoesNotExist, BookChapter.DoesNotExist):
            return redirect('/404/')


class BookRankingView(ListView):
    template_name = 'books/bookranking.html'
    queryset = Book.objects.filter(status=1).order_by('-votes')
    context_object_name = 'books_all'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = list(self.queryset)
        user_auth = self.request.user.is_authenticated
        books = qs[3:]
        books_top = qs[:3]
        context = {
            'books': books, 'books_top': books_top,
            'page_title': 'Ranking',
            'user_auth': user_auth,
        }
        if user_auth:
            user_lib = list(self.request.user.library.book.all())
            context['user_lib'] = user_lib
        return context


class BookSearchView(ListView):
    template_name = 'books/booksearch.html'
    form = BookSearchForm
    context = {'form': form, 'page_title': 'Search for Books'}

    def get(self, request, **kwargs):
        return render(request, template_name=self.template_name, context=self.context)

    def post(self, request, **kwargs):
        form = self.form(request.POST)
        context = {'form': form, 'page_title': 'Search for Books'}
        if form.is_valid():
            field_data = form.cleaned_data['search_field']
            books = Book.objects.filter(title__icontains=field_data)
            context['books'] = books
        else:
            form = self.form()
            context['form'] = form
        return render(request, template_name=self.template_name, context=context)
