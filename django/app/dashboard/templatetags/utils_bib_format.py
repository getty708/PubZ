from django.shortcuts import reverse
from django.utils.safestring import mark_safe
from django.template.exceptions import TemplateDoesNotExist

from django import template
from django.template.loader import get_template
register = template.Library()

from django.db.models import Q
from django.db.models.query import QuerySet
from core.models import Author, AuthorOrder, Book


# ----------------------------------------------------------------------------

# ===================
#  Filter Func.
# ===================

@register.filter(name='test_format')
def test_format(bibtex):
    return bibtex


@register.filter(name='bibtex_tile_format')
def bibtex_tile_format(bib, *args,**kwargs):
    """
    Args.
    -----
    - bibtex: core.Bibtex object
    """
    context = {}
    context["bib"] = bib
    context["book"] = bib.book
    
    # Get Authors
    context["authors"] = bib.authors_list

    # Fill Placeholders
    bib_style = bib.bib_type_key
    try:
        template_name = "custom/bibtex/tile/{}.html".format(bib_style)
        html = get_template(template_name,)
    except TemplateDoesNotExist:
        template_name = "custom/bibtex/tile/{}.html".format("DEFAULT")
        html = get_template(template_name,)
    html = mark_safe(html.render(context))
    return html


@register.filter(name='bibtex_list_format')
def bibtex_list_format(bib, *args,**kwargs):
    """
    Args.
    -----
    - bibtex: core.Bibtex object
    """
    context = {}
    context["bib"] = bib
    context["book"] = bib.book
    
    # Get Authors
    context["authors"] = bib.authors_list

    # Fill Placeholders
    bib_style = bib.bib_type_key
    try:
        template_name = "custom/bibtex/list/{}.html".format(bib_style)
        html = get_template(template_name,)
    except TemplateDoesNotExist:
        template_name = "custom/bibtex/list/{}.html".format("DEFAULT")
        html = get_template(template_name,)
    html = mark_safe(html.render(context))
    return html


@register.filter(name='bibtex_bib_format')
def bibtex_bib_format(bib, *args,**kwargs):
    """
    Args.
    -----
    - bibtex: core.Bibtex object
    """
    context = {}
    context["bib"] = bib
    context["book"] = bib.book
    
    # Get Authors
    context["authors"] = bib.authors_list

    # Display { as variable.
    context["cb_left"] = "{"
    context["cb_right"] = "}"

    # Fill Placeholders
    bib_style = bib.bib_type_key
    try:
        template_name = "custom/bibtex/bibtex/{}.html".format(bib_style)
        html = get_template(template_name,)
    except TemplateDoesNotExist:
        template_name = "custom/bibtex/bibtex/{}.html".format("DEFAULT")
        html = get_template(template_name,)
    html = mark_safe(html.render(context))
    return html    
    # return func(bibtex)()


@register.filter(name='bibtex_latex_format')
def bibtex_latex_format(bib, *args,**kwargs):
    """
    Args.
    -----
    - bibtex: core.Bibtex object
    """
    context = {}
    context["bib"] = bib
    context["book"] = bib.book
    
    # Get Authors
    context["authors"] = bib.authors_list

    # Display { as variable.
    context["cb_left"] = "{"
    context["cb_right"] = "}"

    # Fill Placeholders
    bib_style = bib.bib_type_key
    try:
        template_name = "custom/bibtex/latex/{}.html".format(bib_style)
        html = get_template(template_name,)
    except TemplateDoesNotExist:
        template_name = "custom/bibtex/latex/DEFAULT.html"
        html = get_template(template_name,)
    html = mark_safe(html.render(context))
    return html

# Used for download format
@register.filter(name='bibtex_download_format')
def bibtex_download_format(bib, *args,**kwargs):
    """
    Args.
    -----
    - bibtex: core.Bibtex object
    """
    context = {}
    context["bib"] = bib
    context["book"] = bib.book
    
    # Get Authors
    context["authors"] = bib.authors_list

    # Display { as variable.
    context["cb_left"] = "{"
    context["cb_right"] = "}"

    # Fill Placeholders
    bib_style = bib.bib_type_key
    try:
        template_name = "custom/bibtex/bibdownload/{}.html".format(bib_style)        
        html = get_template(template_name,)
    except TemplateDoesNotExist:
        template_name = "custom/bibtex/latex/DEFAULT.html"    
    html = get_template(template_name,)
    html = mark_safe(html.render(context))
    return html


# ----------------------------------------------------------------------------

# ===================
#  Utils.
# ===================
@register.filter(name='filter_by_book_style')
def filter_by_book_style(bibtex, book_style):
    return [bib for bib in bibtex if bib.bib_type_key == book_style]


@register.filter(name='divide_by_book_style')
def divide_by_book_style(bibtexs,):
    def _filter(bibtexs, _q):
        if isinstance(bibtexs, QuerySet):
            bibs = bibtexs.filter(
                Q(bib_type=_q) |
                Q(book__style=_q)
            )
        elif isinstance(bibtexs, list):
            bibs = [b for b in bibtexs if (b.bib_type == _q) or (b.book.style == _q)]
        else:
            raise ValueError("Unexpected bibtex type. expected QuerySet or list, but got {}".format(type(bibtex)))
        return bibs
                
    def _search(t, ret):
        if isinstance(t[0], str) and isinstance(t[1], str):
            bibs = _filter(bibtexs, t[0])
            if len(bibs) > 0:
                ret.append((t[0],t[1],bibs))
        elif isinstance(t[0], str):
            ret = _search(t[1], ret)
        else:
            for t2 in t:
                ret = _search(t2, ret)
        return ret
    
    ret = []
    for t in Book.STYLE_CHOICES:
        ret = _search(t, ret)
    return ret    
                    
