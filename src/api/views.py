from core.models import Bibtex
from django.views import generic


class IndexView(generic.ListView):
    template_name = "api/index_list.html"
    context_object_name = "latest_bibtex_list"

    def get_queryset(self):
        return Bibtex.objects.order_by("-pub_date", "title_en", "title_ja")
