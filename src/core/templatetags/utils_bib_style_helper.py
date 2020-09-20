from django.shortcuts import reverse
from django.utils.safestring import mark_safe
from django import template
from django.template.loader import get_template
register = template.Library()


# -------
#  Bib
# -------
@register.filter
def remove_brace(value):
    """ Remove braces  (which indicete capital leters in latex).

    Args:
        value (str): string which have ``{``, ``}``.

    Returns:
        str (``{``, ``}`` is removed.)

    Examples:

        >>> val = "The {CNN}-based ..."
        >>> remove_brace(val)
        "The CNN-based ..."

    """
    value = str(value).replace("{", "").replace("}", "")
    return value


@register.filter
def replace_double_hyphen(value):
    """ Replace ``--`` (double) with ``-`` (single).

    Args:
        value (str): string which have ``--``.

    Returns:
        str (``--`` is replaced with ``-``.)

    Examples:

        >>> val = "123--456"
        >>> replace_double_hyphen(val)
        "123-456"

    """
    value = str(value).replace("--", "-")
    return value


# --------
#  Author
# --------
@register.filter
def author_en_default(val):
    """ Returns the author name in the order of (1) given name, (2) family name.

    Args: 
        val (str): name string.

    Returns:
        str

    Examples:

        >>> # Example1: with comma
        >>> name = "Handai, Taro"
        >>> author_en_default(name)
        "Taro Handai"
        >>> # Example2: w/o comma
        >>> name2 = "Taro Handai"
        >>> author_en_default(name)
        "Taro Handai"

    """
    val = str(val)
    vals = [s.strip() for s in val.split(",")]
    if len(vals) == 2:
        return "{} {}".format(vals[1].title(), vals[0].title())
    return val


@register.filter
def author_en_google(val):
    """ Returns the author name in the Google Scholar style (e.g. Taro Handai => T. Handai).

    Args: 
        val (str): name string.

    Returns:
        str

    Examples:

        >>> # Example1: with comma
        >>> name = "Handai, Taro"
        >>> author_en_google(name)
        "T. Handai"
        >>> # Example2: w/o comma and with middle name.
        >>> name2 = "Taro Adam Handai"
        >>> author_en_google(name)
        "T. Handai"

    """
    val = str(val)
    val = [v.strip() for v in val.split(",")]
    if len(val) >= 2:
        # with comma
        family = val[0].split()[-1].title()
        first = val[1][0].upper()
        return "{}. {}".format(first, family)

    # w/o comma
    val = val[0].split()
    if len(val) >= 2:
        return "{}. {}".format(val[0], val[1])
    else:
        return " ".join(val)
