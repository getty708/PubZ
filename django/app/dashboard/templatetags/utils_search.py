from django import template

from django.db.models import Q
from core.models import Author, Bibtex, Book, AuthorOrder, Tag

import datetime

register = template.Library()


@register.inclusion_tag('dashboard/components/search_box.html')
def search_box(display_mode, query_params,*args, **kwargs):
    return {
        "display_mode": display_mode,
        "query_params": query_params
    }

def perse_get_query_params(req):
    """
     Args.
     -----
     - req: requestobject
     -
     Return.
     -------
     - QuerySet, request_dict
    """
    ##return get query
    if "keywords" in req.GET:
        keywords = req.GET.get("keywords")
    else:
        keywords = None
    if "book_style" in req.GET:
        book_style = req.GET.get("book_style")
    else:
        book_style = None
    if "order" in req.GET:
        order = req.GET.get("order")
    else:
        order = None
    if "pubdate_start" in req.GET:
        pubdate_start = req.GET.get("pubdate_start")
        if pubdate_start!="":
            pd_start_list = pubdate_start.split("-")
            pubdate_start_field = datetime.date(int(pd_start_list[0]), int(pd_start_list[1]), int(pd_start_list[2]))
        else:
            pubdate_start_field = None
    else:
<<<<<<< HEAD
=======
        pubdate_start = None
>>>>>>> feature-view
        pubdate_start_field = None
    if "pubdate_end" in req.GET:
        pubdate_end = req.GET.get("pubdate_end")
        if pubdate_end!="":
            pd_end_list = pubdate_end.split("-")
            pubdate_end_field = datetime.date(int(pd_end_list[0]), int(pd_end_list[1]), int(pd_end_list[2]))
        else:
            pubdate_end_field = None
    else:
<<<<<<< HEAD
        pubdate_end_field = None

    ##query params save
    query_param_dic = {"keywords":keywords       }
=======
        pubdate_end = None
        pubdate_end_field = None

    ##query params save
    query_param_dic = {"keywords":keywords,"book_style":book_style,"order":order,"pubdate_start":pubdate_start,"pubdate_end":pubdate_end}
>>>>>>> feature-view

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
        bibtex_queryset = keywords_filtering(bibtex_queryset,keywords)

    #order
    if order==None:
<<<<<<< HEAD
        return bibtex_queryset.order_by('-pub_date', 'title_en', 'title_ja')
    elif order=="ascending":
        return bibtex_queryset.order_by('-pub_date', 'title_en', 'title_ja')
    elif order=="desending":
        return bibtex_queryset.order_by('pub_date', 'title_en', 'title_ja')
=======
        return bibtex_queryset.order_by('-pub_date', 'title_en', 'title_ja'),query_param_dic
    elif order=="ascending":
        return bibtex_queryset.order_by('-pub_date', 'title_en', 'title_ja'),query_param_dic
    elif order=="desending":
        return bibtex_queryset.order_by('pub_date', 'title_en', 'title_ja'),query_param_dic
>>>>>>> feature-view


def keywords_filtering(bibtex_queryset, keywords):

    keywords_list = keywords.split(" ")

    for one_keyword in keywords_list:
        bibtex_queryset = bibtex_queryset.filter(
            Q(title_en__icontains=one_keyword) |
            Q(title_ja__icontains=one_keyword) |
            Q(book__title__icontains=one_keyword) |
            Q(authors__name_en__icontains=one_keyword) |
            Q(authors__name_ja__icontains=one_keyword) |
            Q(note__icontains=one_keyword)
        ).distinct()

    return bibtex_queryset
