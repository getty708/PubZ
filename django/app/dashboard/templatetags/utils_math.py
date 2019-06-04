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
@register.simple_tag(name='substract')
def substract(a, b):
    return a - b


@register.simple_tag(name='multiply')
def multiply(a, b):
    return a * b
