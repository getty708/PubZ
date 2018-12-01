from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views import generic

import datetime
from datetime import datetime

from core.models import Author, Bibtex, Book, AuthorOrder, Tag
from notification import alert
from dashboard.forms import BibtexForm
from django.db.models import Q

from dashboard.templatetags import utils_search as utils

"""
Bibtex
"""
class IndexView(generic.ListView):

    def get_queryset(self):

        query_set,self.query_param_dic = utils.perse_get_query_params(self.request)

        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["book_style_list"] = ["INTPROC","JOURNAL","CONF_DOMESTIC","CONF_DOMESTIC_NO_REVIEW","CONF_NATIONAL","BOOK","KEYNOTE","NEWS","OTHERS","AWARD"]
        context["query_params"] = self.query_param_dic
        context["year"] = datetime.now().year
        return context

class IndexViewList(IndexView):

    template_name = 'dashboard/bibtex/index_list.html'
    context_object_name = 'latest_bibtex_list'


class IndexViewTable(IndexView):
    template_name = 'dashboard/bibtex/index_tab.html'
    context_object_name = 'latest_bibtex_list'

class IndexViewBib(IndexView):
    template_name = 'dashboard/bibtex/index_bib.html'
    context_object_name = 'latest_bibtex_list'

class IndexViewLatex(IndexView):
    template_name = 'dashboard/bibtex/index_latex.html'
    context_object_name = 'latest_bibtex_list'


class DetailView(generic.DetailView):
    model = Bibtex
    template_name = 'dashboard/detail.html'


"""
Book
"""
class BookIndexView(generic.ListView):
    template_name = 'dashboard/book/index.html'
    context_object_name = 'latest_book_list'

    def get_queryset(self):
        return Book.objects.order_by('title')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["book_style_list"] = ["INTPROC","JOURNAL","CONF_DOMESTIC","CONF_DOMESTIC_NO_REVIEW","CONF_NATIONAL","BOOK","KEYNOTE","NEWS","OTHERS","AWARD"]
        return context


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'dashboard/book/detail.html'




"""
Author
"""
class AuthorIndexView(generic.ListView):
    template_name = 'dashboard/author/index.html'
    context_object_name = 'latest_author_list'

    def get_queryset(self):
        return Author.objects.order_by('name_en')


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'dashboard/author/detail.html'

"""
Tag
"""
class TagIndexView(generic.ListView):
    template_name = 'dashboard/tag/index.html'
    context_object_name = 'latest_tag_list'

    def get_queryset(self):
        return Tag.objects.order_by('name')

class TagDetailView(generic.DetailView):
    model = Tag
    template_name = 'dashboard/tag/detail.html'


"""
Notification
"""
def notification_alert(request):
    msg = False
    # Send Email
    status = alert.send_email_test()
    return render(request,
                  'notification/alert.html',
                  {
                      'msg': msg,
                      'status': status,
                  })
