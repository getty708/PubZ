from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
from django.views import generic


from core.models import Bibtex


class IndexView(generic.ListView):
    template_name = 'api/index_list.html'
    context_object_name = 'latest_bibtex_list'

    def get_queryset(self):
        return Bibtex.objects.order_by('-pub_date', 'title_en', 'title_ja')
