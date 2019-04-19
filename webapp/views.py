from django.shortcuts     import render, reverse
from django.views.generic import TemplateView

from django.http          import HttpResponseRedirect

class HomeView(TemplateView):
    template_name = 'index.html'

    def post(self, request, *args, **kwargs):
        search_text = request.POST.get('search_text')
        return HttpResponseRedirect(reverse('home'))
