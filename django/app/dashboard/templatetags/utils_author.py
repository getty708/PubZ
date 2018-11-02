from django.shortcuts import reverse
from django.utils.safestring import mark_safe

from django import template
register = template.Library()

from core.models import Author, AuthorOrder

from dashboard.templatetags.utils_bib_format import BibtexFormatBase


# ==================
#  Custom Author View
# ==================
class BibtexFormatAuthorDefault(BibtexFormatBase):

    def get_template_INTPROC(self):
        html = (
            '{authors}, '
        )
        return html

    def get_template_JOURNAL(self):
        html = (
            '{authors}, '
        )
        return html

    def get_template_CONF_DOMESTIC(self):
        html = (
            '{authors}, '
        )
        return html

    def get_template_CONF_DOMESTIC_NO_REVIEW(self):
        html = (
            '{authors}, '
        )
        return html

    def get_template_NATIONAL(self):
        html = (
            '{authors}, '
        )
        return html

    def get_template_BOOK(self):
        html = (
            '{authors}, '
        )
        return html

    def get_template_KEYNOTE(self):
        html = (
            '{authors}, '
        )
        return html

    def get_template_NEWS(self):
        html = (
            '{authors}, '
        )
        return html

    def get_template_OTHERS(self):
        html = (
            '{authors}, '
        )
        return html

    def get_template_AWARD(self):
        html = (
            '{authors}, '
        )
        return html


# ----------------------------------------------------------------------------

# ===================
#  Filter Func.
# ===================
@register.filter(name='bibtex_author_format')
def bibtex_author_format(bibtex, func=BibtexFormatAuthorDefault, *args,**kwargs):
    """
    Args.
    -----
    - bibtex: core.Bibtex object
    """
    return func(bibtex)()

