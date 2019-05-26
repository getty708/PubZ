from django import template


from django.db.models import Q
from core.models import Author, Bibtex, Book, AuthorOrder, Tag

import datetime

register = template.Library()


@register.inclusion_tag('dashboard/components/search_box.html')
def search_box(display_mode, query_params, *args, **kwargs):
    return {
        "display_mode": display_mode,
        "GET_params": query_params,
    }

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
        "book_style",
        "sort",
        # "pubyear",
        # "pubyear_all",
        # "pubyear_type",
        "period_method",
        "period_year",
        "tags",
        "display_style",
    ]

    
    params = {}
    for key in GET_param_keys:
        params[key] = req.GET.get(key, None)
           
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
            print("keyword: ", keyword)
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
    
    # Sort
    sort = params.get('sort')
    if sort == None:
        return bibtex_queryset.order_by('-pub_date','title_en','title_ja')
    elif sort == "ascending":
        return bibtex_queryset.order_by('-pub_date', 'title_en', 'title_ja')
    elif sort == "desending":
        return bibtex_queryset.order_by('pub_date', 'title_en', 'title_ja')
    
