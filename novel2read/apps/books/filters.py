from .models import Book

import django_filters


class BookFilter(django_filters.FilterSet):
    COUNTRY_CHOICES = (
        ('china', 'China'),
        ('korea', 'Korea'),
        ('japan', 'Japan'),
    )
    CHAPTER_FILTER = (
        ('low', 'Lowest'),
        ('high', 'Highest'),
    )
    VOTES_FILTER = (
        ('low', 'Lowest'),
        ('high', 'Highest'),
    )
    RATING_FILTER = (
        (1, 'more than 1 star'),
        (2, 'more than 2 star'),
        (3, 'more than 3 star'),
        (4, 'more than 4 star'),
    )

    country = django_filters.ChoiceFilter(label='Country', choices=COUNTRY_CHOICES, method='filter_by_country')
    chapters = django_filters.ChoiceFilter(label='Chapters', choices=CHAPTER_FILTER, method='filter_by_chapters')
    votes = django_filters.ChoiceFilter(label='Votes', choices=VOTES_FILTER, method='filter_by_votes')
    rating = django_filters.ChoiceFilter(label='Rating', choices=RATING_FILTER, method='filter_by_rating')

    class Meta:
        model = Book
        fields = {'status_release'}

    def __init__(self, *args, **kwargs):
        super(BookFilter, self).__init__(*args, **kwargs)
        self.filters['status_release'].label = 'Completion'

    def filter_by_country(self, qs, name, value):
        qs = qs if not value else qs.filter(country__iexact=value)
        return qs

    def filter_by_chapters(self, qs, name, value):
        expression = 'chapters' if value == 'low' else '-chapters'
        return qs.order_by(expression)

    def filter_by_votes(self, qs, name, value):
        expression = 'chapters' if value == 'low' else '-chapters'
        return qs.order_by(expression)

    def filter_by_rating(self, qs, name, value):
        qs = qs if not value else qs.filter(rating__gte=value)
        return qs
