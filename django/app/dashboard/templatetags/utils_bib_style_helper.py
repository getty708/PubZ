from django.shortcuts import reverse
from django.utils.safestring import mark_safe

from django import template
from django.template.loader import get_template
register = template.Library()


"""
Bib
"""
@register.filter
def remove_brace(value):
    # Captal
    value = value.replace("{", "").replace("}", "")
    return value


"""
Author
"""
@register.filter
def author_en_default(val):
    vals = [s.strip() for s in val.split(",")]
    if len(vals) == 2:
        return "{} {}".format(vals[1], vals[0])
    return val


@register.filter
def author_en_google(val):
    # Google Scholar  Style
    val = [v.strip() for v in val.split(",")]
    if len(val) == 2:
        family = val[0].title()
        first = val[1][0].upper()
        return "{}. {}".format(first, family)
    else:
        return " ".join(val)

