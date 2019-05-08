from django.db.models import Count
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdminMixin
from .models import BookGenre, BookTag, Book, BookChapter


@admin.register(BookGenre)
class BookGenreAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_display = ('name', 'get_bookcount', 'created', 'modified', )
    readonly_fields = ('slug', 'get_bookcount', 'created', 'modified', )

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'get_bookcount'),
        }),
        (None, {
            'fields': ('created', 'modified', ),
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.prefetch_related('books').annotate(Count('book'))
        return qs

    def get_bookcount(self, obj):
        return obj.book__count
    get_bookcount.short_description = 'Books Count'
    get_bookcount.admin_order_field = 'book__count'


@admin.register(BookTag)
class BookTagAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_display = ('name', 'get_bookcount', 'created', 'modified', )
    readonly_fields = ('slug', 'get_bookcount', 'created', 'modified', )
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'get_bookcount'),
        }),
        (None, {
            'fields': ('created', 'modified', ),
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.prefetch_related('books').annotate(Count('books'))
        return qs

    def get_bookcount(self, obj):
        return obj.books__count
    get_bookcount.short_description = 'Books Count'
    get_bookcount.admin_order_field = 'books__count'


@admin.register(Book)
class BookAdmin(SummernoteModelAdminMixin, admin.ModelAdmin):
    fields = (
        ('title', 'title_sm', 'slug'),
        ('status', 'status_release'),
        'bookgenre',
        'booktag',
        'allow_comments',
        ('author', 'country'),
        'poster',
        ('rating', 'ranking', 'votes', 'recommended'),
        'description',
        ('volumes', 'chapters_count'),
        ('visit', 'visit_id', 'visited'),
        ('revisit', 'revisit_id', 'revisited'),
    )
    summernote_fields = ('description', )
    readonly_fields = ('slug', 'chapters_count', )
    filter_horizontal = ('booktag', )
    list_select_related = ('bookgenre', )
    list_display = ('title', 'get_bookgenre', 'recommended', 'chapters_count', 'status', 'visited', 'visit_id', 'revisited', 'revisit_id', 'created', 'modified', )

    def get_bookgenre(self, obj):
        return obj.bookgenre.name
    get_bookgenre.short_description = 'Book Genre'
    get_bookgenre.admin_order_field = 'bookgenre'


@admin.register(BookChapter)
class BookChapterAdmin(SummernoteModelAdminMixin, admin.ModelAdmin):
    summernote_fields = ('text', )
    readonly_fields = ('slug', 'c_id', )
    list_select_related = ('book', )
    list_display = ('title', 'c_id', 'get_book', 'created', 'modified', )

    def get_book(self, obj):
        return obj.book.title
    get_book.short_description = 'Book'
    get_book.admin_order_field = 'book'
