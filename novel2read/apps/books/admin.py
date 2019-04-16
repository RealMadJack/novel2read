from django.contrib import admin
from django_summernote.admin import SummernoteModelAdminMixin
from .models import BookGenre, BookTag, Book, BookChapter


@admin.register(BookGenre)
class BookGenreAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', )
    list_display = ('name', 'created', 'modified', )


@admin.register(BookTag)
class BookTagAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', )
    list_display = ('name', 'created', 'modified', )


@admin.register(Book)
class BookAdmin(SummernoteModelAdminMixin, admin.ModelAdmin):
    fields = (
        ('title', 'title_sm', 'slug'),
        ('status', 'status_release'),
        'bookgenre',
        'booktag',
        ('author', 'country'),
        'poster',
        ('rating', 'ranking', 'votes'),
        'description',
        ('volumes', 'chapters'),
        ('visited', 'visited_id'),
        ('revisit', 'revisit_id'),
        ('visited_wn', 'id_wn'),
        ('visited_bn', 'id_bn'),
    )
    summernote_fields = ('description', )
    readonly_fields = ('slug', 'chapters', )
    filter_horizontal = ('booktag', )
    list_select_related = ('bookgenre', )
    list_display = ('title', 'get_bookgenre', 'chapters', 'status', 'id_wn', 'id_bn', 'visited_wn', 'visited_bn', 'created', 'modified', )

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
