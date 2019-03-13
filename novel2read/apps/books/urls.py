from django.urls import path
from django.views.generic import TemplateView

from .apps import BooksConfig
from .views import *

app_name = BooksConfig.name

urlpatterns = [
    path("", TemplateView.as_view(template_name="books/front_page.html"), name="front_page"),
    path("category/", TemplateView.as_view(template_name="books/browse.html"), name="browse"),
    path("ranking/", TemplateView.as_view(template_name="books/ranking.html"), name="ranking"),
    path("search/", TemplateView.as_view(template_name="books/search.html"), name="search"),
]
