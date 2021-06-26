from django import template
from django.template.loader import get_template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def print_bibtexs(
    context,
    style=False,
):
    """Render bibtexs in the selected style.

    At first. this function load a template of the selected display style
    (e.g. list, tile). Then render and return the html object.

    Args:
        context (context): django cotnext object.
        style (str, optional): keyword of a display style (e.g. list, tile, bibtex).
            (default: False)

    Returns:
        rendered html object.

    """

    # GET Params
    display_style = context.get("display_style", "list")
    if isinstance(style, str):
        display_style = style

    # Get a template and Render
    template_name = "custom/bibtex/{}/index.html".format(display_style)
    try:
        html = get_template(template_name)
    except IndentationError:
        template_name = "custom/bibtex/list/index.html"
        html = get_template(template_name)

    html = mark_safe(
        html.render(
            {
                "latest_bibtex_list": context["latest_bibtex_list"],
            }
        )
    )
    return html
