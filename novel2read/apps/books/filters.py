from .models import Book

import django_filters


class BookFilter(django_filters.FilterSet):
    class Meta:
        model = Book
        fields = {
            'rating': ['lt', 'gt'],
            'chapters': ['lt', 'gt']
        }
