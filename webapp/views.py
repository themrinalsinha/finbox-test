from django.shortcuts     import render
from django.views.generic import TemplateView
from django.http          import HttpResponseRedirect, JsonResponse
from django.conf          import settings
from os.path              import exists, join

from .utils               import FinboxSearch
from .models              import FoodReviews

class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if not exists(join(settings.PROJECT_DIR, 'finbox.db')) or not exists(join(settings.INV_INDEX)):
            context['db_missing'] = True
            return self.render_to_response(context)

        search_text = request.POST.get('search_text', None)
        context['search_string'] = search_text if search_text else ''
        if search_text:
            documents = FinboxSearch(search_text).search()
            pk_list   = [x.get('pk') for x in documents]
            context['reviews'] = FoodReviews.objects.filter(pk__in=pk_list) if pk_list else None
        else:
            context['reviews'] = None
        return self.render_to_response(context)
