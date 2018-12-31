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
        self.GET_params = utils.parse_GET_params(self.request)
        query_set = utils.get_bibtex_query_set(self.GET_params)
        self.GET_params["num_hits"] = len(query_set)
        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['GET_params'] = self.GET_params
        context["year"] = datetime.now().year
        return context

class IndexViewList(IndexView):

    template_name = 'dashboard/bibtex/index.html'
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
    template_name = 'dashboard/bibtex/detail.html'


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


def notification_alert_author(request, author_id, bibtex_id):
    msg = False
    # Send Email
    status = False

    subject = "Please update the registration information."
    message = "The following papers have missing items.\n\n\n"

    bibtex_queryset = Bibtex.objects.get(id=bibtex_id)
    bibtex_name = bibtex_queryset.title_en

    author_queryset = Author.objects.get(id=author_id)
    author_mail = author_queryset.mail

    status = alert.send_email_to_appointed_address(author_mail, bibtex_queryset)

    return render(request,
                  'notification/alert.html',
                  {
                      'msg': msg,
                      'status': status,
                      'author': author_mail,
                      'bibtex': bibtex_name,
                      'subject': subject,
                      'message': message,
                  })


def notification_alert_all(request):
    msg = False
    subject = "Please update the registration information."
    message = "The following papers have missing items.\n\n\n"

    status, not_published_list = alert.send_email_to_all()

    return render(request,
                  'notification/alert_all.html',
                  {
                      'msg': msg,
                      'status': status,
                      'bibtexs': not_published_list,
                      'subject': subject,
                      'message': message,
                  })
