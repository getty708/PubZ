from core.models import Bibtex, Book
from django import template
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import get_template
from django.utils.safestring import mark_safe

register = template.Library()


# ===================
#  Filter Func.
# ===================
@register.filter(name="bibtex_tile_format")
def bibtex_tile_format(bib, *args, **kwargs):
    """This template tag renders a single bibtex object in a tile style.

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
        html = get_template(
            template_name,
        )
    html = mark_safe(html.render(context))
    return html


@register.filter(name="bibtex_list_format")
def bibtex_list_format(bib, *args, **kwargs):
    """This template tag renders a single bibtex object in a list style.

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
        html = get_template(
            template_name,
        )
    except TemplateDoesNotExist:
        template_name = "custom/bibtex/list/{}.html".format("DEFAULT")
        html = get_template(
            template_name,
        )
    html = mark_safe(html.render(context))
    return html


@register.filter(name="bibtex_bib_format")
def bibtex_bib_format(bib, *args, **kwargs):
    """This template tag renders a single bibtex object in a bibtex style.

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
        html = get_template(
            template_name,
        )
    except TemplateDoesNotExist:
        template_name = "custom/bibtex/bibtex/{}.html".format("DEFAULT")
        html = get_template(
            template_name,
        )
    html = mark_safe(html.render(context))
    return html
    # return func(bibtex)()


@register.filter(name="bibtex_latex_format")
def bibtex_latex_format(bib, *args, **kwargs):
    """This template tag renders a single bibtex object in a latex style.

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
        html = get_template(
            template_name,
        )
    except TemplateDoesNotExist:
        template_name = "custom/bibtex/latex/DEFAULT.html"
        html = get_template(
            template_name,
        )
    html = mark_safe(html.render(context))
    return html


# ===================
#  utils.
# ===================
@register.filter(name="filter_by_book_style")
def filter_by_book_style(bibtexs, book_style):
    """Returns bibtex objects of the selected book type.

    Args:
        bibtexs (list of core.models.Bibtex): queryset of Bibtex.
        book_style (str): book style key (e.g. JOUNRAL)

    Returns:
        list of Bibtex objectsxs

    """
    return [bib for bib in bibtexs if bib.bib_type_key == book_style]


def expand_book_style_tuple(choices):
    """
    Args:
        choises (tuple): Book.STYLE_CHOICES

    Returns:
        tuple: 2d

    """
    choices_ret = []
    for t in choices:
        if isinstance(t[0], str) and isinstance(t[1], tuple):
            for t2 in t[1]:
                choices_ret.append(t2)
    return choices_ret


@register.filter(name="split_bibtexs_by_bib_style")
def split_bibtexs_by_bib_style(bibtexs):
    """

    Args:
        bibtexs (list of Queryset of Bibtex):

    Returns:
        list of tuple: (Style Key, Display Name, Bibtex List)

    """
    # Get STYLE KYES
    bibtex_backet = dict()

    choices = expand_book_style_tuple(Book.STYLE_CHOICES) + list(
        Bibtex.BIBSTYLE_CHOICES
    )
    for i, (key, _) in enumerate(choices):
        # if key == "SAME_AS_BOOK":
        #     _idx_same_as_book = i
        if key != "SAME_AS_BOOK":
            bibtex_backet[key] = []
    choices.pop(i)

    # Split by Style
    for bib in bibtexs:
        bibtex_backet[bib.bib_type_key].append(bib)

    # Make list of tuple
    ret = []
    for key, display_name in choices:
        if len(bibtex_backet[key]) > 0:
            ret.append((key, display_name, bibtex_backet[key]))
    return ret
