from django.shortcuts import reverse
from django.utils.safestring import mark_safe

from django import template
from django.template.loader import get_template
register = template.Library()



@register.filter
def remove_brace(value):
    # Captal
    value = value.replace("{", "").replace("}", "")
    return value
