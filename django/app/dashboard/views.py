from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.urls import resolve

import datetime
from datetime import datetime
import urllib

from core.models import Author, Bibtex, Book, AuthorOrder, Tag
from notification import alert
from dashboard.forms import BibtexForm
from django.db.models import Q

from dashboard.templatetags import utils_search as utils

"""
Bibtex
"""
class IndexView(generic.ListView):
    template_name = 'dashboard/bibtex/index.html'
    context_object_name = 'latest_bibtex_list'
    
    def get_queryset(self):
        self.GET_params = utils.parse_GET_params(self.request)
        query_set = utils.get_bibtex_query_set(self.GET_params)
        self.GET_params["num_hits"] = len(query_set)
        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['GET_params'] = self.GET_params
        current_url_name = resolve(self.request.path_info).url_name
        if current_url_name != "index":
            context["display_style"] = current_url_name.split("_")[-1]
        context["year"] = datetime.now().year
        return context


class DetailView(generic.DetailView):
    model = Bibtex
    template_name = 'dashboard/bibtex/detail.html'


"""
Book
"""
class BookIndexView(generic.ListView):
    template_name = 'dashboard/book/index.html'
    context_object_name = 'latest_book_list'
    paginate_by = 30
 
    def get_queryset(self):
        self.selected_style = self.request.GET.get("style", "ALL")
        styles = [s[0] for s in Book.STYLE_CHOICES]
        key = self.selected_style if self.selected_style in styles else False
        if key:
            return Book.objects.filter(style=key,).order_by('title')
        return Book.objects.order_by('title')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        style_active = None
        for i, style in enumerate(Book.STYLE_CHOICES):
            if style[0] == self.selected_style:
                style_active = (i, style[0], style[1],)
                continue
        context["style"] = style_active if isinstance(style_active, tuple) else (0, "ALL", "All",)
        context["styles"] = Book.STYLE_CHOICES
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
    paginate_by = 30

    def get_queryset(self):
        self.search_keyword = self.request.GET.get("keyword",)
        if self.search_keyword:
            self.search_keyword = urllib.parse.unquote(self.search_keyword)
            return Author.objects.filter(
                Q(name_en__icontains=self.search_keyword) |
                Q(name_ja__icontains=self.search_keyword) |
                Q(dep_en__icontains=self.search_keyword)  |
                Q(dep_ja__icontains=self.search_keyword)
            ).order_by('name_en')
        return Author.objects.order_by('name_en')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_keyword"] = self.search_keyword
        return context


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
