from django.shortcuts import render
from django.views.generic import View, ListView


class FrontPageView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, template_name='books/front_page.html', context=context)


class GenrePageView(ListView):
    pass
