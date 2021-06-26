import datetime

from core.models import Bibtex, Book
from django import template
from django.db.models import Q

register = template.Library()


@register.inclusion_tag("dashboard/components/search_box.html")
def search_box(display_mode, query_params, user, *args, **kwargs):
    """ Template tag to render the search box.  """
    return {
        "display_mode": display_mode,
        "GET_params": query_params,
        "user": user,
    }


@register.simple_tag()
def get_bib_style_keys():
    """ Returns bibtex/book style keys for search box. """

    def _parse(t, ret):
        if len(t) > 1 and isinstance(t[0], str) and isinstance(t[1], str):
            if t[0] != "SAMEASBOOK":
                ret.append(
                    (
                        t[0],
                        t[1],
                    )
                )
        elif isinstance(t[0], str) and isinstance(t[1], tuple):
            ret.append(
                (
                    t[0],
                    "header",
                )
            )
            ret = _parse(t[1], ret)
        else:
            for t2 in t:
                ret = _parse(t2, ret)

        return ret

    ret = _parse(Book.STYLE_CHOICES, [])
    ret.append(
        (
            "Others",
            "header",
        )
    )
    ret = _parse(Bibtex.BIBSTYLE_CHOICES, ret)
    return ret


def parse_GET_params(req):
    """Parse GET parameters and returns dict with search params.

    Args:
        req (requestobject)

    Returns:
        dict

    """
    GET_param_keys = [
        # key, default value,
        ("keywords", None),
        ("book_style", None),
        ("sort", None),
        ("period_method", "ACADEMIC_YEAR"),
        ("period_year", datetime.datetime.now().year),
        ("tags", None),
        ("display_style", None),
    ]
    period_method_exists = "period_method" in req.GET.keys()
    params = {}
    for key, default_val in GET_param_keys:
        params[key] = req.GET.get(key, default_val)

    # == Validation ==
    try:
        params["period_year"] = int(params["period_year"])
    except ValueError:
        params["period_year"] = datetime.datetime.now().year

    if params["period_method"] == "ACADEMIC_YEAR":
        if not period_method_exists:
            if datetime.datetime.now().month < 4:
                # NOTE: Translate to the academic year if the page was accessed
                # between January and March.
                params["period_year"] -= 1

    # == For usability ==
    if params["keywords"] is not None:
        params["period_method"] = "ALL"
    return params


def get_bibtex_query_set(params):
    """Returns bibtex objects which match the search parameters.

    Args:
        params: dict which is maded by `parse_GET_params`

    Returns:
        QuerySet
        request_dict

    """
    bibtex_queryset = Bibtex.objects.all()

    # Book_style
    book_style = params.get("book_style")
    if (book_style is not None) and (book_style != "ALL"):
        # TODO: Make it more better (remove if sentence)
        if (book_style == "AWARD") or (book_style == "KEYNOTE"):
            bibtex_queryset = bibtex_queryset.filter(bib_type=book_style)
        else:
            bibtex_queryset = bibtex_queryset.filter(
                book__style=book_style,
                bib_type="SAMEASBOOK",
            )

    # Filter by published year
    period_method = params.get("period_method", "ACADEMIC_YEAR")
    year = params.get("period_year", datetime.datetime.now().year)
    if period_method == "YEAR":
        bibtex_queryset = bibtex_queryset.filter(
            pub_date__gte=datetime.date(int(year), 1, 1),
            pub_date__lte=datetime.date(int(year), 12, 31),
        )
    elif period_method == "ACADEMIC_YEAR":
        bibtex_queryset = bibtex_queryset.filter(
            pub_date__gte=datetime.date(int(year), 4, 1),
            pub_date__lte=datetime.date(int(year) + 1, 3, 31),
        )
    else:
        pass

    # Keywords
    keywords = params.get("keywords")
    if keywords is not None:
        keywords_list = keywords.split(" ")
        for keyword in keywords_list:
            bibtex_queryset = bibtex_queryset.filter(
                Q(title__icontains=keyword)
                | Q(book__title__icontains=keyword)
                | Q(book__abbr__icontains=keyword)
                | Q(authors__name_en__icontains=keyword)
                | Q(authors__name_ja__icontains=keyword)
            ).distinct()

    # Tags
    tags = params.get("tags")
    if tags is not None:
        tags_list = tags.split(" ")
        for tag in tags_list:
            bibtex_queryset = bibtex_queryset.filter(
                Q(tags__name__icontains=tag)
            ).distinct()

    # Sort
    sort = params.get("sort")
    if sort is None:
        return bibtex_queryset.order_by("-pub_date", "book", "title")
    elif sort == "ascending":
        return bibtex_queryset.order_by("-pub_date", "book", "title")
    elif sort == "desending":
        return bibtex_queryset.order_by("pub_date", "book", "title")
