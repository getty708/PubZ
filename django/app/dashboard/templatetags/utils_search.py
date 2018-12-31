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
    if "pubyear_type" in req.GET:
        pubyear_type = req.GET.get("pubyear_type")
    else:
        pubyear_type = None
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
            if pubyear_type==None:
                bibtex_queryset = bibtex_queryset.filter(pub_date__gte=datetime.date(int(pubyear), 1, 1), pub_date__lte=datetime.date(int(pubyear), 12, 31))
            else:
                bibtex_queryset = bibtex_queryset.filter(pub_date__gte=datetime.date(int(pubyear), 4, 1), pub_date__lte=datetime.date(int(pubyear)+1, 3, 31))

    #keywords
    if keywords!=None:
        bibtex_queryset = keywords_filtering(bibtex_queryset,keywords)

    #tags
    if tags != None:
        bibtex_queryset = tags_filtering(bibtex_queryset, tags)

    ##query params save
    query_param_dic = {"keywords":keywords,"book_style":book_style,"order":order, "pubyear":pubyear,"pubyear_all": pubyear_all,"pubyear_type": pubyear_type,"tags": tags,"hits_num": str(bibtex_queryset.count()) }

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




# -------------------
def parse_GET_params(req):
    """
     Args.
     -----
     - req: requestobject
     -
     Return.
     -------
     - dict: {key:value}
    """
    GET_param_keys = [
        "keywords",
        "book_sytle",
        "order",
        "pubyear",
        "pubyear_all",
        "pubyear_type",
        "tags",
        "display_style",
    ]

    
    params = {}
    for key in GET_param_keys:
        params[key] = req.GET.get(key, None)

    if (params['pubyear_all'] == None) and (params['pubyear'] == None):
        params['pubyear'] = datetime.datetime.now().year #now_year
    return params


def get_bibtex_query_set(params):
    """
    Args.
    -----
    - params: dict which is maded by `parse_GET_params`
    
    Return.
    -------
    - QuerySet, request_dict
    """
    bibtex_queryset = Bibtex.objects.all()

    # Book_style
    book_style = params.get('book_style')
    if (not book_style == None) and (not book_style == "ALL"):
        bibtex_queryset = bibtex_queryset.filter(book__style=book_style)

    # Pubyear
    pubyear      = params.get('pubyear')
    pubyear_all  = params.get('pubyear_all')
    pubyear_type = params.get('pubyear_type')
    if pubyear_all == None:
        if not pubyear == None:
            if pubyear_type==None:
                bibtex_queryset = bibtex_queryset.filter(
                    pub_date__gte=datetime.date(int(pubyear), 1, 1),
                    pub_date__lte=datetime.date(int(pubyear), 12, 31)
                )
            else:
                bibtex_queryset = bibtex_queryset.filter(
                    pub_date__gte=datetime.date(int(pubyear), 4, 1),
                    pub_date__lte=datetime.date(int(pubyear)+1, 3, 31)
                )
                
    # Keywords
    keywords = params.get('keywords')
    if keywords!=None:
        keywords_list = keywords.split(" ")        
        for keyword in keywords_list:
            bibtex_queryset = bibtex_queryset.filter(
                Q(title_en__icontains=keyword) |
                Q(title_ja__icontains=keyword) |
                Q(book__title__icontains=keyword) |
                Q(authors__name_en__icontains=keyword) |
                Q(authors__name_ja__icontains=keyword) |
                Q(note__icontains=keyword)
            ).distinct()

    # Tags
    tags = params.get('tags')
    if tags != None:
        tags_list = tags.split(" ")
        for tag in tags_list:
            bibtex_queryset = bibtex_queryset.filter(
                Q(tags__name__icontains=tag)
            ).distinct()        
    
    # Order
    order = params.get('order')
    if order == None:
        return bibtex_queryset.order_by('-pub_date','title_en','title_ja')
    elif order == "ascending":
        return bibtex_queryset.order_by('-pub_date', 'title_en', 'title_ja')
    elif order == "desending":
        return bibtex_queryset.order_by('pub_date', 'title_en', 'title_ja')
    
