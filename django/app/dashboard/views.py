from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views import generic



from core.models import Bibtex


class IndexView(generic.ListView):
    template_name = 'dashboard/index.html'
    context_object_name = 'latest_bibtex_list'

    def get_queryset(self):
        return Bibtex.objects.order_by('-pub_date')[:5]
    

class DetailView(generic.DetailView):
    model = Bibtex
    template_name = 'dashboard/detail.html'    
    
