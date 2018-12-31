from django import template
from django.template.loader import get_template
from django.utils.safestring import mark_safe

from core.models import Author, Bibtex, Book, AuthorOrder, Tag
import datetime


register = template.Library()


@register.simple_tag(takes_context=True)
def print_bibtexs(context,):
    print(dict(Book.STYLE_CHOICES))
    template_name = "custom/bibtex/list/index.html"
    html = get_template(template_name,)
    html = mark_safe(html.render({
        'latest_bibtex_list': context['latest_bibtex_list'],
        'book_styles': dict(Book.STYLE_CHOICES),
    }))
    return html
