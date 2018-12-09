from django import template

from django.db.models import Q
from core.models import Author, Bibtex, Book, AuthorOrder, Tag

import datetime

register = template.Library()


@register.inclusion_tag('dashboard/components/search_box.html')
def search_box(display_mode, query_params, *args, **kwargs):
    return {
        "display_mode": display_mode,
        "query_params": query_params,
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
    if "pubyear" in req.GET:
        pubyear = req.GET.get("pubyear")
        if pubyear=="":
            pubyear = None
    else:
        pubyear = None
    if "pubyear_all" in req.GET:
        pubyear_all = req.GET.get("pubyear_all")
    else:
        pubyear_all = None
        if pubyear==None:
            pubyear = datetime.datetime.now().year#now_year
    if "tags" in req.GET:
        tags = req.GET.get("tags")
    else:
        tags = None

    ##filtering
    bibtex_queryset = Bibtex.objects.all()

    #book_style
    if book_style!=None and book_style!="ALL":
        bibtex_queryset = bibtex_queryset.filter(book__style=book_style)

    #pubyear
    if pubyear_all==None:
        if pubyear!=None:
            bibtex_queryset = bibtex_queryset.filter(pub_date__gte=datetime.date(int(pubyear), 1, 1), pub_date__lte=datetime.date(int(pubyear), 12, 31))

    #keywords
    if keywords!=None:
        bibtex_queryset = keywords_filtering(bibtex_queryset,keywords)

    #tags
    if tags != None:
        bibtex_queryset = tags_filtering(bibtex_queryset, tags)

    ##query params save
    query_param_dic = {"keywords":keywords,"book_style":book_style,"order":order, "pubyear":pubyear,"pubyear_all": pubyear_all,"tags": tags,"hits_num": str(bibtex_queryset.count()) }

    #order
    if order==None:
        return bibtex_queryset.order_by('-pub_date', 'title_en', 'title_ja'),query_param_dic
    elif order=="ascending":
        return bibtex_queryset.order_by('-pub_date', 'title_en', 'title_ja'),query_param_dic
    elif order=="desending":
        return bibtex_queryset.order_by('pub_date', 'title_en', 'title_ja'),query_param_dic


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


def tags_filtering(bibtex_queryset, tags):
    tags_list = tags.split(" ")

    for tag in tags_list:
        bibtex_queryset = bibtex_queryset.filter(
            Q(tags__name__icontains=tag)
        ).distinct()

    return bibtex_queryset
