from django.shortcuts import reverse
from django.utils.safestring import mark_safe

from django import template
from django.template.loader import get_template
register = template.Library()

from core.models import Author, AuthorOrder, Book


# ----------------------------------------------------------------------------

# ===================
#  Filter Func.
# ===================

@register.filter(name='test_format')
def test_format(bibtex):
    return bibtex

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
    authors =  AuthorOrder.objects.filter(bibtex=bib).order_by('order')
    context["authors"] = [author.author for author in authors]

    # Fill Placeholders
    bib_style = bib.book.style    
    template_name = "custom/bibtex/list/{}.html".format(bib_style)
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
    authors =  AuthorOrder.objects.filter(bibtex=bib).order_by('order')
    context["authors"] = [author.author for author in authors]

    # Display { as variable.
    context["cb_left"] = "{"
    context["cb_right"] = "}"

    # Fill Placeholders
    bib_style = bib.book.style    
    template_name = "custom/bibtex/bibtex/{}.html".format(bib_style)
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
    authors =  AuthorOrder.objects.filter(bibtex=bib).order_by('order')
    context["authors"] = [author.author for author in authors]

    # Display { as variable.
    context["cb_left"] = "{"
    context["cb_right"] = "}"

    # Fill Placeholders
    bib_style = bib.book.style    
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
    authors =  AuthorOrder.objects.filter(bibtex=bib).order_by('order')
    context["authors"] = [author.author for author in authors]

    # Display { as variable.
    context["cb_left"] = "{"
    context["cb_right"] = "}"

    # Fill Placeholders
    bib_style = bib.book.style    
    template_name = "custom/bibtex/bibdownload/{}.html".format(bib_style)
    html = get_template(template_name,)
    html = mark_safe(html.render(context))
    return html    
    # return func(bibtex)()


# ----------------------------------------------------------------------------

# ===================
#  Utils.
# ===================
@register.filter(name='filter_by_book_style')
def filter_by_book_style(bibtex, book_style):
    return bibtex.filter(book__style=book_style)
