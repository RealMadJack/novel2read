from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
from django.db.models import F
from django.http import JsonResponse
# from django.utils.decorators import method_decorator
from django.urls import reverse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
# from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import View, DetailView, ListView

from .models import Book, BookTag, BookChapter
from .forms import BookSearchForm
from .utils import capitalize_slug
from novel2read.apps.users.models import BookProgress


class FrontPageView(View):
    def get(self, request, *args, **kwargs):
        books = Book.objects.published().prefetch_related('bookchapters')
        context = {'books': books}
        return render(request, template_name='books/front_page.html', context=context)


class BookGenreView(ListView):
    template_name = 'books/bookgenre.html'

    def get(self, request, *args, **kwargs):
        try:
            books = Book.objects.published().select_related('bookgenre').prefetch_related('booktag').order_by('-votes')
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
                tag_name = capitalize_slug(kwargs['booktag_slug'])
                books = Book.objects.published().filter(booktag__slug=kwargs['booktag_slug'])
                books = books.select_related('bookgenre').prefetch_related('booktag').order_by('-votes')
                context['tag_name'] = tag_name
                context['books'] = books
            return render(request, template_name=self.template_name, context=context)
        except BookTag.DoesNotExist:
            return redirect('/404/')


class BookView(DetailView):
    template_name = 'books/book.html'

    def get(self, request, *args, **kwargs):
        try:
            book = Book.objects.select_related('bookgenre').prefetch_related('booktag', 'bookchapters').get(slug=kwargs['book_slug'])
            bookchapters = list(book.bookchapters.all())
            first_chap = bookchapters[0] if len(bookchapters) >= 1 else None
            last_chap = bookchapters[-1] if len(bookchapters) >= 1 else None
            user_auth = request.user.is_authenticated
            context = {
                'book': book, 'bookchapters': bookchapters,
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
    """
    TODO: refactor next-prev-chap: bookchaps in list and slicing
    """

    template_name = 'books/bookchapter.html'

    def get(self, request, *args, **kwargs):
        try:
            c_id = kwargs['c_id']
            bookchapters = BookChapter.objects.filter(book__slug=kwargs['book_slug']).select_related('book')
            cached_qs = list(bookchapters)
            try:
                bookchapter = cached_qs[c_id - 1:c_id][0]
            except IndexError:
                if cached_qs:
                    bookchapter = cached_qs[0]
                else:
                    return redirect('/404/')
            try:
                prev_chap = cached_qs[c_id - 2:c_id - 1][0]
            except IndexError:
                prev_chap = None
            try:
                next_chap = cached_qs[c_id:c_id + 2][0]
            except IndexError:
                next_chap = None
            context = {
                'bookchapters': bookchapters,
                'bookchapter': bookchapter,
                'prev_chap': prev_chap, 'next_chap': next_chap}
            if request.user.is_authenticated:
                context['user_lib'] = list(request.user.library.book.all())
                try:
                    book_prog = BookProgress.objects.get(user=request.user, book=bookchapter.book)
                    if book_prog.c_id != bookchapter.c_id:
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
    queryset = Book.objects.published().order_by('-votes')
    context_object_name = 'books_all'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = list(self.queryset.iterator())
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
        context = dict(self.context)  # update get view context
        context['form'] = form

        if request.is_ajax():
            data = {}
            template_name = 'books/booksearch-result.html'
            search_field = request.POST.get('search_field', None)

            if not search_field:
                # handle ajax error
                return JsonResponse(data, status=403)

            books = Book.objects.published().annotate(
                search=SearchVector('title', 'description'),
            ).filter(search=search_field)
            context['books'] = books
            context['s_result'] = f"<p>Didn't find book: <b>{search_field}</b></p>" if not books else ''
            data['html_search_form_result'] = render_to_string(
                template_name,
                context=context,
                request=request
            )
            return JsonResponse(data)

        if form.is_valid():
            field_data = form.cleaned_data['search_field']
            books = Book.objects.published().annotate(
                search=SearchVector('title', 'description'),
            ).filter(search=field_data)
            context['s_result'] = f"<p>Didn't find book: <b>{search_field}</b></p>" if not books else ''
            context['books'] = books
        return render(request, template_name=self.template_name, context=context)


@login_required
def book_vote_view(request, *args, **kwargs):
    if request.method == "POST":
        try:
            user = request.user
            book = Book.objects.get(slug=kwargs['book_slug'])
            book_rev = reverse('books:book', kwargs={'book_slug': kwargs['book_slug']})
            next_url = request.POST.get('next', book_rev)
            if user.profile.votes <= 0:
                print('user reached vote limit')
            else:
                user.profile.votes = F('votes') - 1
                user.save()
                book.votes += 1
                book.save()
            return redirect(next_url)
        except Book.DoesNotExist:
            return redirect('/404/')
    return redirect('/400/')


@login_required
def book_vote_ajax_view(request, *args, **kwargs):
    data = {'is_valid': False}

    if request.is_ajax():
        user = request.user
        user_votes = user.profile.votes
        book = Book.objects.get(slug=kwargs['book_slug'])
        if user_votes <= 0:
            data['info_msg'] = 'You have no votes for today.'
        else:
            try:
                data['is_valid'] = True
                data['user_votes'] = int(user_votes) - 1
                data['book_votes'] = int(book.votes) + 1
                user.profile.votes = F('votes') - 1
                user.save()
                book.votes = F('votes') + 1
                book.save()
            except Exception as e:
                data['error'] = str(e)
    return JsonResponse(data)
