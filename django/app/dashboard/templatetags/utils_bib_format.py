from django.shortcuts import reverse
from django.utils.safestring import mark_safe
from django.template.exceptions import TemplateDoesNotExist

from django import template
from django.template.loader import get_template
register = template.Library()

from django.db.models import Q
from django.db.models.query import QuerySet
from core.models import Author, AuthorOrder, Book

# ===================
#  Filter Func.
# ===================

@register.filter(name='bibtex_tile_format')
def bibtex_tile_format(bib, *args,**kwargs):
    """ This template tag renders a single bibtex object in a tile style.    

    The tile styleis a visually rich format. 
    This template tag select tamplate based on bibtex's ``bib_type``.
   
    Args:
        bibtex (core.Bibtex): core.Bibtex object

    Example:
        .. code-block:: html

            {% bibtex_tile_format bibtex %}

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
        html = get_template(template_name)
    except TemplateDoesNotExist:
        template_name = "custom/bibtex/tile/{}.html".format("DEFAULT")
        html = get_template(template_name,)
    html = mark_safe(html.render(context))
    return html


@register.filter(name='bibtex_list_format')
def bibtex_list_format(bib, *args,**kwargs):
    """ This template tag renders a single bibtex object in a list style.    
    
    Args:
        bibtex (core.Bibtex): core.Bibtex object

    Example:
        .. code-block:: html

            {% bibtex_list_format bibtex %}

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
    """ This template tag renders a single bibtex object in a bibtex style.    
    
    Args:
        bibtex (core.Bibtex): core.Bibtex object

    Example:
        .. code-block:: html

            {% bibtex_bib_format bibtex %}

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
    """ This template tag renders a single bibtex object in a latex style.    
    
    Args:
        bibtex (core.Bibtex): core.Bibtex object

    Example:
        .. code-block:: html

            {% bibtex_latex_format bibtex %}

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



# ===================
#  utils.
# ===================
@register.filter(name='filter_by_book_style')
def filter_by_book_style(bibtexs, book_style):
    """ Returns bibtex objects of the selected book type.

    Args:
        bibtexs (list of core.models.Bibtex): queryset of Bibtex.
        book_style (str): book style key (e.g. JOUNRAL)

    Returns:
        list of Bibtex objectsxs

    """
    return [bib for bib in bibtexs if bib.bib_type_key == book_style]


@register.filter(name='divide_by_book_style')
def divide_by_book_style(bibtexs):
    """ 

    Todo:
        replace ``_filter`` private function with ``filter_by_book_style``

    """
    
    def _filter(bibtexs, _q):
        """ 
        
        Doing the same things as filter_by_book_style
        
        Args:
            bibtexs (list or queryset): list of Bibtex objects
            _q (str): book style key (e.g. JOUNRAL)

        Returns:
            list or queryset of Bibtex objects.
        
        """
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
        """

        Args:
            t (tuple of str): tuple of Book's STYLE_CHOICE (e.g. ('JOURNAL', 'Journal'))
            ret (list of tuple): store resules to this list.
        
        Returns:
            list of tuple

        """
        
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
                    
