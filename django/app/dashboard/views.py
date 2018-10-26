from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views import generic

import datetime

from core.models import Author, Bibtex, Book, AuthorOrder, Tag
from notification import alert
from dashboard.forms import BibtexForm
from django.db.models import Q
"""
Bibtex
"""
class IndexView(generic.ListView):

    def keywords_filtering(self, bibtex_queryset, keywords):

        keywords_list = keywords.split(" ")

        for one_keyword in keywords_list:
            bibtex_queryset = bibtex_queryset.filter(
                Q(title_en__icontains=one_keyword) |
                Q(title_ja__contains=one_keyword) |
                Q(book__title__icontains=one_keyword) |
                Q(authors__name_en__icontains=one_keyword) |
                Q(authors__name_ja__icontains=one_keyword) |
                Q(note__icontains=one_keyword)
            ).distinct()

        return bibtex_queryset

    def get_queryset(self):
        ##get query
        if "keywords" in self.request.GET:
            keywords = self.request.GET.get("keywords")
        else:
            keywords = None
        if "book_style" in self.request.GET:
            book_style = self.request.GET.get("book_style")
        else:
            book_style = None
        if "order" in self.request.GET:
            order = self.request.GET.get("order")
        else:
            order = None
        if "pubdate_start" in self.request.GET:
            pubdate_start = self.request.GET.get("pubdate_start")
            if pubdate_start!="":
                pd_start_list = pubdate_start.split("-")
                pubdate_start_field = datetime.date(int(pd_start_list[0]), int(pd_start_list[1]), int(pd_start_list[2]))
            else:
                pubdate_start_field = None
        else:
            pubdate_start_field = None
        if "pubdate_end" in self.request.GET:
            pubdate_end = self.request.GET.get("pubdate_end")
            if pubdate_end!="":
                pd_end_list = pubdate_end.split("-")
                pubdate_end_field = datetime.date(int(pd_end_list[0]), int(pd_end_list[1]), int(pd_end_list[2]))
            else:
                pubdate_end_field = None
        else:
            pubdate_end_field = None

        ##filtering
        bibtex_queryset = Bibtex.objects.all()

        #book_style
        if  book_style!=None and book_style!="ALL":
            bibtex_queryset = bibtex_queryset.filter(book__style=book_style)

        #pubdate
        if pubdate_start_field!=None and pubdate_end_field!=None:
            bibtex_queryset = bibtex_queryset.filter(pub_date__gte=pubdate_start_field, pub_date__lte=pubdate_end_field)
        elif pubdate_start_field!=None:
            bibtex_queryset = bibtex_queryset.filter(pub_date__gte=pubdate_start_field)
        elif pubdate_end_field!=None:
            bibtex_queryset = bibtex_queryset.filter(pub_date__lte=pubdate_end_field)

        #keywords
        if keywords!=None:
            bibtex_queryset = self.keywords_filtering(bibtex_queryset,keywords)

        #order
        if order==None:
            return bibtex_queryset.order_by('-pub_date', 'title_en', 'title_ja')
        elif order=="ascending":
            return bibtex_queryset.order_by('-pub_date', 'title_en', 'title_ja')
        elif order=="desending":
            return bibtex_queryset.order_by('pub_date', 'title_en', 'title_ja')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["book_style_list"] = ["INTPROC","JOURNAL","CONF_DOMESTIC","CONF_DOMESTIC_NO_REVIEW","CONF_NATIONAL","BOOK","KEYNOTE","NEWS","OTHERS","AWARD"]
        return context

class IndexViewList(IndexView):

    template_name = 'dashboard/index.html'
    context_object_name = 'latest_bibtex_list'

"""class AddTestDatas(generic.TemplateView):###for test

    #add test kanren ha,
    #urls no add to
    #kono class to
    #for_test directory dake
    #kono 3 tu wo keseba ok

    template_name = 'dashboard/for_test/add_test_datas.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if Bibtex.objects.all().exists():
            context["exists"] = "Already added"
        else:
            context["exists"] = "no data"
        return context

    ##add Tag
    tag1 = Tag(name="Clustering",description="for clustering")
    tag2 = Tag(name="Wikipedia",description="for wikipedia")
    tag1.save()
    tag2.save()

    ##add author
    author_1 = Author(name_en='Tatsuya Nakamura', dep_en='Osaka University',mail="mail@mail.co.jp")
    author_1.save()
    author_2 = Author(name_en='Takahiro Hara', dep_en='Osaka University',mail="mail@mail.co.jp")
    author_2.save()

    ##add book
    book1 = Book(title="ACM Transactions on Asian and Low-Resource Language Information Processing",style="INTPROC")
    book2 = Book(title="IEEE",style="JOURNAL")
    book1.save()
    book2.save()

    ##add bibtex
    bibtex1 = Bibtex(language='EN', title_en='Wikipedia-Based Relatedness Measurements for Multilingual Short Text Clustering',book=book1,volume=3,number=5,chapter=1,page="10-20")
    bibtex2 = Bibtex(language='JA', title_ja='wikipediaのクラスタリング(ジャーナル)',book=book2,volume=2,number=2,chapter=2,page="15-24")
    bibtex1.save()
    bibtex2.save()

    ##add AuthorOrder
    AuthorOrder(bibtex=bibtex1,author=author_1,order=1).save()
    AuthorOrder(bibtex=bibtex1,author=author_2,order=2).save()
    #AuthorOrder(bibtex=bibtex2,author=author_1,order=1).save()
    #AuthorOrder(bibtex=bibtex2,author=author_2,order=2).save()"""

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
