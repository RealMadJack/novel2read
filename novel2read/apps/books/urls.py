from django.urls import path
from django.views.generic import TemplateView

from .apps import BooksConfig
from .views import *

app_name = BooksConfig.name

urlpatterns = [
    path("", TemplateView.as_view(template_name="books/front_page.html"), name="front_page"),
    path("category/", TemplateView.as_view(template_name="books/browse.html"), name="browse"),
    path(
        "category/<slug:bookgenre_slug>/",
        TemplateView.as_view(template_name="books/browse.html"),
        name="genre"
    ),
    path("tags/", TemplateView.as_view(template_name="books/browse.html"), name="browse1"),
    path(
        "tags/<slug:booktag_slug>/",
        TemplateView.as_view(template_name="books/browse.html"),
        name="tag"
    ),
    path("books/", TemplateView.as_view(template_name="books/browse.html"), name="browse2"),
    path(
        "books/<slug:book_slug>/",
        TemplateView.as_view(template_name="books/browse.html"),
        name="book"
    ),
    path("ranking/", TemplateView.as_view(template_name="books/ranking.html"), name="ranking"),
    path("search/", TemplateView.as_view(template_name="books/search.html"), name="search"),
]
