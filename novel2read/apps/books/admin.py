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
    readonly_fields = ('slug', 'chapters', )
    filter_horizontal = ('booktag', )
    list_display = ('title', 'get_bookgenre', 'created', 'modified', )

    def get_bookgenre(self, obj):
        return obj.bookgenre.name
    get_bookgenre.short_description = 'Book Genre'
    get_bookgenre.admin_order_field = 'bookgenre'


@admin.register(BookChapter)
class BookChapterAdmin(admin.ModelAdmin):
    model = BookChapter
    readonly_fields = ('slug', 'count_id', )
    list_display = ('title', 'get_book', 'created', 'modified', )

    def get_book(self, obj):
        return obj.book.title
    get_book.short_description = 'Book'
    get_book.admin_order_field = 'book'
