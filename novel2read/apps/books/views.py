from django.shortcuts import render
from django.views.generic import TemplateView


class FrontPageView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, template_name='books/front_page.html', context={})
