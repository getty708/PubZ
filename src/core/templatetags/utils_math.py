from django import template

register = template.Library()

# ===================
#  Filter Func.
# ===================


@register.simple_tag(name="substract")
def substract(a, b):
    """Returns substraction result. :math:`(a - b)`

    Args:
        a, b (int or float)

    Returns:
        int or float

    """
    return a - b


@register.simple_tag(name="multiply")
def multiply(a, b):
    """ Returns multiplication results. :math:`a * b` """
    return a * b
