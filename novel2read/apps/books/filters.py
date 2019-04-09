from .models import Book

import django_filters


class BookFilter(django_filters.FilterSet):
    """
    country: choices(china, korea, japan) -> instance.country.lower()
    chapters: chapters min / max
    votes(popular): votes min / max
    rating: rating min / max
    """
    COUNTRY_CHOICES = (
        ('china', 'China'),
        ('korea', 'Korea'),
        ('japan', 'Japan'),
    )

    country = django_filters.ChoiceFilter(label='Country', choices=COUNTRY_CHOICES, method='filter_by_country')

    class Meta:
        model = Book
        fields = {'status_release'}

    def __init__(self, *args, **kwargs):
        super(BookFilter, self).__init__(*args, **kwargs)
        self.filters['status_release'].label = 'Type'

    def filter_by_country(self, qs, name, value):
        qs = qs if not value else qs.filter(country__iexact=value)
        return qs
