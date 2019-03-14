from django.urls import path
from django.views.generic import TemplateView

from .apps import BooksConfig
from .views import FrontPageView, GenrePageView

app_name = BooksConfig.name

urlpatterns = [
    path("", FrontPageView.as_view(), name="front_page"),
    path("category/all/", GenrePageView.as_view(), name="genre-all"),
    path(
        "category/<slug:bookgenre_slug>/",
        GenrePageView.as_view(),
        name="genre"
    ),
    path("tags/", TemplateView.as_view(template_name="books/genre.html"), name="browse1"),
    path(
        "tags/<slug:booktag_slug>/",
        TemplateView.as_view(template_name="books/genre.html"),
        name="tag"
    ),
    path("books/", TemplateView.as_view(template_name="books/genre.html"), name="browse2"),
    path(
        "books/<slug:book_slug>/",
        TemplateView.as_view(template_name="books/genre.html"),
        name="book"
    ),
    path(
        "books/<slug:book_slug>/<int:bookchapter_pk>/",
        TemplateView.as_view(template_name="books/genre.html"),
        name="bookchapter"
    ),
    path("ranking/", TemplateView.as_view(template_name="books/ranking.html"), name="ranking"),
    path("search/", TemplateView.as_view(template_name="books/search.html"), name="search"),
]
