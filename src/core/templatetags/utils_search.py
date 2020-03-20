import datetime
from django import template
register = template.Library()
from django.db.models import Q

from core.models import Author, Bibtex, Book, AuthorOrder, Tag


@register.inclusion_tag('dashboard/components/search_box.html')
def search_box(display_mode, query_params, user,  *args, **kwargs):
    """ Template tag to render the search box.  """
    return {
        "display_mode": display_mode,
        "GET_params": query_params,
        "user": user,
    }

@register.simple_tag()
def get_bib_style_keys():
    """ Returns bibtex/book style keys for search box. """
    
    def _parse(t, ret):
        if len(t) > 1 and isinstance(t[0], str) and isinstance(t[1], str):
            if t[0] != "SAMEASBOOK":
                ret.append((t[0],t[1],))
        elif isinstance(t[0], str) and isinstance(t[1], tuple):
            ret.append((t[0],'header',))
            ret = _parse(t[1], ret)
        else:
            for t2 in t:
                ret = _parse(t2, ret)
                
        return ret

    ret = _parse(Book.STYLE_CHOICES, [])
    ret.append(("Others", "header",))
    ret = _parse(Bibtex.BIBSTYLE_CHOICES, ret)
    return ret

def parse_GET_params(req):
    """ Parse GET parameters and returns dict with search params.

     Args:
         req (requestobject)

     Returns:
         dict

    """
    GET_param_keys = [
        "keywords","book_style","sort",
        "period_method","period_year",
        "tags","display_style",
    ]
    
    params = {}
    for key in GET_param_keys:
        params[key] = req.GET.get(key, None)        
    return params


def get_bibtex_query_set(params):
    """ Returns bibtex objects which match the search parameters.

    Args:
        params: dict which is maded by `parse_GET_params`
    
    Returns:
        QuerySet
        request_dict

    """
    bibtex_queryset = Bibtex.objects.all()

    # Book_style
    book_style = params.get('book_style')
    if (not book_style == None) and (not book_style == "ALL"):
        # TODO: Make it more better (remove if sentence)
        if (book_style == "AWARD") or (book_style == "KEYNOTE"):
            bibtex_queryset = bibtex_queryset.filter(bib_type=book_style)
        else:
            bibtex_queryset = bibtex_queryset.filter(
                book__style=book_style, bib_type="SAMEASBOOK",)
        

    # Filter by published year
    period_method = params.get('period_method', 'all')
    if period_method == "year":
        year = params.get('period_year', datetime.datetime.now().year)
        bibtex_queryset = bibtex_queryset.filter(
            pub_date__gte=datetime.date(int(year), 1,1),
            pub_date__lte=datetime.date(int(year), 12,31),
        )
    elif period_method == "fiscal_year":
        year = params.get('period_year', datetime.datetime.now().year)
        bibtex_queryset = bibtex_queryset.filter(
            pub_date__gte=datetime.date(int(year), 4,  1),
            pub_date__lte=datetime.date(int(year)+1, 3, 31),
        )
    else:
        pass
    
    # Keywords
    keywords = params.get('keywords')
    if keywords!=None:
        keywords_list = keywords.split(" ")        
        for keyword in keywords_list:
            bibtex_queryset = bibtex_queryset.filter(
                Q(title_en__icontains=keyword) |
                Q(title_ja__icontains=keyword) |
                Q(book__title__icontains=keyword) |
                Q(book__abbr__icontains=keyword) |
                Q(authors__name_en__icontains=keyword) |
                Q(authors__name_ja__icontains=keyword)
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
    
