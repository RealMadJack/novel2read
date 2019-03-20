from django.contrib import admin
from .models import BookGenre, BookTag, Book, BookChapter


@admin.register(BookGenre)
class BookGenreAdmin(admin.ModelAdmin):
    model = BookGenre
    readonly_fields = ('slug', )
    list_display = ('name', 'created', 'modified', )


@admin.register(BookTag)
class BookTagAdmin(admin.ModelAdmin):
    model = BookTag
    readonly_fields = ('slug', )
    list_display = ('name', 'created', 'modified', )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    model = Book
    fields = (
        ('title', 'title_sm', 'slug'),
        'bookgenre',
        'booktag',
        ('author', 'country'),
        'poster_url',
        ('rating', 'ranking'),
        'description',
        ('volumes', 'chapters', 'chapters_max'),
        ('visited_wn', 'book_id_wn'),
        ('visited_bn', 'book_id_bn'),
        ('status', 'status_release'),
    )
    readonly_fields = ('slug', 'chapters', )
    filter_horizontal = ('booktag', )
    list_select_related = ('bookgenre', )
    list_display = ('title', 'get_bookgenre', 'chapters', 'status', 'book_id_wn', 'book_id_bn', 'visited_wn', 'visited_bn', 'created', 'modified', )

    def get_bookgenre(self, obj):
        return obj.bookgenre.name
    get_bookgenre.short_description = 'Book Genre'
    get_bookgenre.admin_order_field = 'bookgenre'


@admin.register(BookChapter)
class BookChapterAdmin(admin.ModelAdmin):
    model = BookChapter
    readonly_fields = ('slug', )
    list_select_related = ('book', )
    list_display = ('title', 'get_book', 'created', 'modified', )

    def get_book(self, obj):
        return obj.book.title
    get_book.short_description = 'Book'
    get_book.admin_order_field = 'book'
