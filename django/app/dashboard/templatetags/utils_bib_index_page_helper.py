from django import template
from django.template.loader import get_template
from django.utils.safestring import mark_safe

from core.models import Author, Bibtex, Book, AuthorOrder, Tag
import datetime


register = template.Library()

# --------------------------------------------------------------
@register.simple_tag(takes_context=True)
def print_bibtexs(context,):
    # GET Params
    params = context["GET_params"]
    print(params)
    display_style = params.get('display_style', 'list')
    if not display_style:
        display_style = 'list'
    
    # Get a template and Render
    template_name = "custom/bibtex/{}/index.html".format(display_style)
    html = get_template(template_name,)
    html = mark_safe(html.render({
        'latest_bibtex_list': context['latest_bibtex_list'],
        'book_styles': dict(Book.STYLE_CHOICES),
    }))
    return html


# # -----------------------------------------------------------
# def parse_GET_query_params(request):
#     pass
