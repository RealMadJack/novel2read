from django.urls import path
from django.views.generic import TemplateView

from .apps import BooksConfig
from .views import FrontPageView, BookGenreView, BookTagView, BookView, BookChapterView

app_name = BooksConfig.verbose_name

urlpatterns = [
    path("", FrontPageView.as_view(), name="front_page"),
    path("category/all/", BookGenreView.as_view(), name="genre-list"),
    path(
        "category/<slug:bookgenre_slug>/",
        BookGenreView.as_view(),
        name="genre"
    ),
    path("tags/all/", BookTagView.as_view(), name="tag-list"),
    path("tags/<slug:booktag_slug>/", BookTagView.as_view(), name="tag"),
    path("books/<slug:book_slug>/", BookView.as_view(), name="book"),
    path("books/<slug:book_slug>/<int:bookchapter_pk>/", BookChapterView.as_view(), name="bookchapter"),
    path("ranking/", TemplateView.as_view(template_name="books/ranking.html"), name="ranking"),
    path("search/", TemplateView.as_view(template_name="books/search.html"), name="search"),
]
