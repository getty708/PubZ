from django.shortcuts import reverse
from django.utils.safestring import mark_safe

from django import template
register = template.Library()

from core.models import Author, AuthorOrder

"""
Bibtex Format Filter
"""
# ==================
#  Base Class
# ==================
class BibtexFormatBase(object):
    def __init__(self, bibtex, *args, **kwargs):
        self.bibtex = bibtex
        self.style = bibtex.book.style
        self.url_bib = reverse("dashboard:bib_detail", kwargs={'pk':bibtex.id})

    def __call__(self):
        # Convert Bibtex object into dict
        bibtex = self.bibtex
        context = bibtex.__dict__

        if bibtex.language == "EN":
            context['title'] = bibtex.title_en
        elif bibtex.language == "JA":
            context['title'] = bibtex.title_ja

        context['citekey'] = "test_id"
        context['url_bib'] = self.url_bib
        context['book_title'] = bibtex.book.title
 
        try:
            context['year'] = bibtex.pub_date.year
            context['month'] = bibtex.pub_date.month
            context['month_string'] = self.get_string_month(bibtex.pub_date.month)
        except AttributeError:
            context['year']  = "None"
            context['month'] = "None"
            context['month_string'] = "None"
        context['publisher'] = bibtex.book.publisher
        
        # Get Authors
        authors = AuthorOrder.objects.filter(bibtex=bibtex).order_by('order')
        context["authors"] = self.get_html_authors(authors)
        # Fill Placeholders
        html_template = self.get_template()
        html = html_template.format(**context)
        return mark_safe(html)


    def get_template(self,):
        try:
            html = eval('self.get_template_{}()'.format(self.style))
        except AttributeError:
            html = self.get_template_DEFAULT()
        return html

    #
    #  Template
    def get_author_name(self, author):
        """
        Args.
        -----
        - author: Author Object

        Return.
        --------
        - Name String
        """
        if self.bibtex.language == 'EN':
            name = author.name_en
        else:
            name = author.name_ja
        return name


    def get_html_authors(self, authors):
        """
        Args.
        -----
        - authors: QuerySet of AuthorOrder

        Return
        ------
        - HTML String of author's part
        """
        template = '<a href="{url}">{name}</a>'
        html = ''
        if len(authors) == 0:
            return "None"
        for i, author in enumerate(authors):
            name = self.get_author_name(author.author)
            url = reverse("dashboard:author_detail",
                          kwargs={'pk':author.author.id})
            html += template.format(url=url,name=name)
            if not i+1 == len(authors):
                html += ', '
        return html


    def get_template_DEFAULT(self):
        html = (
            '{authors}; '
            '<a href="{url_bib}">"{title}"</a>, '
            '(Default Style)'
        )
        return html


    def get_string_month(self, month_int):

        month_list = ["January","Febrary","March","April","May","June","July","August","September","October","November","December"]

        return month_list[month_int -1]


# ==================
#  Custom List View
# ==================
class BibtexFormatListDefault(BibtexFormatBase):

    def get_template_INTPROC(self):
        html = (
            '{authors}, '
            '<a href="{url_bib}">"{title},"</a> '
            '{book_title}, '
            'volume {volume}, '
            'number {number}, '
            'pages {page} {month_string} {year}.'
        )
        return html

    def get_template_JOURNAL(self):
        html = (
            '{authors}, '
            '<a href="{url_bib}">"{title},"</a> '
            '{book_title}, '
            'volume {volume}, '
            'number {number}, '
            'pages {page} {month_string} {year}.'
        )
        return html

    def get_template_CONF_DOMESTIC(self):
        html = (
            '{authors}, '
            '<a href="{url_bib}">"{title},"</a> '
            '{book_title}, '
            'pages {page} {year}年{month}月.'
        )
        return html

    def get_template_CONF_DOMESTIC_NO_REVIEW(self):
        html = (
            '{authors}, '
            '<a href="{url_bib}">"{title},"</a> '
            '{book_title}, '
            'pages {page} {year}年{month}月.'
        )
        return html

    def get_template_NATIONAL(self):
        html = (
            '{authors}, '
            '<a href="{url_bib}">"{title},"</a> '
            '{book_title}, '
            '{year}年{month}月.'
        )
        return html

    def get_template_BOOK(self):
        html = (
            '{authors}, '
            '<a href="{url_bib}">"{title},"</a> '
            '{book_title}, '
            'pages {page} {month_string} {year}.'
        )
        return html

    def get_template_KEYNOTE(self):
        html = (
            '{authors}, '
            '<a href="{url_bib}">"{title},"</a> '
            '{book_title}, '
            '{year}年{month}月.'
        )
        return html

    def get_template_NEWS(self):
        html = (
            '{authors}, '
            '<a href="{url_bib}">"{title},"</a> '
            '{book_title}, '
            '{year}年{month}月.'
        )
        return html

    def get_template_OTHERS(self):
        html = (
            '{authors}, '
            '<a href="{url_bib}">"{title},"</a> '
            '{book_title}, '
            'volume {volume}, '
            'number {number}, '
            '{page} {year}年{month}月.'
        )
        return html

    def get_template_AWARD(self):
        html = (
            '{authors}, '
            '<a href="{url_bib}">"{title},"</a> '
            '{book_title}, '
            '{year}年{month}月.'
        )
        return html


# ====================
#  Custom Bibtex View
# ====================
class BibtexFormatBibtexDefault(BibtexFormatBase):

    def get_template_DEFAULT(self):
        html = [
            '<pre class="mb-0" >',
            '@article{{{citekey},',
            '  title = {{{title}}},',
            '  author = {{{authors}}},',
            '  journal = {{{book_title}}},',
            '  volume = {{{volume}}},',
            '  number = {{{number}}},',
            '  pages = {{{page}}},',
            '  year = {{{year}}},',
            '  publisher = {{{publisher}}},',
            '}}',
            '</pre>',
        ]
        return "\n".join(html)

    def get_template_INTPROC(self):
        html = [
            '<pre class="mb-0" >',
            '@inproceedings{{{citekey},',
            '  title = {{{title}}},',
            '  author = {{{authors}}},',
            '  booktitle = {{{book_title}}},',
            '  volume = {{{volume}}},',
            '  number = {{{number}}},',
            '  pages = {{{page}}},',
            '  month = {{{month}}},',
            '  year = {{{year}}},',
            '}}',
            '</pre>',
        ]
        return "\n".join(html)

    def get_template_JOURNAL(self):
        html = [
            '<pre class="mb-0" >',
            '@article{{{citekey},',
            '  title = {{{title}}},',
            '  author = {{{authors}}},',
            '  journal = {{{book_title}}},',
            '  volume = {{{volume}}},',
            '  number = {{{number}}},',
            '  pages = {{{page}}},',
            '  month = {{{month}}},',
            '  year = {{{year}}},',
            '}}',
            '</pre>',
        ]
        return "\n".join(html)

    def get_template_CONF_DOMESTIC(self):
        html = [
            '<pre class="mb-0" >',
            '@inproceedings{{{citekey},',
            '  title = {{{title}}},',
            '  author = {{{authors}}},',
            '  booktitle = {{{book_title}}},',
            '  volume = {{{volume}}},',
            '  number = {{{number}}},',
            '  pages = {{{page}}},',
            '  month = {{{month}}},',
            '  year = {{{year}}},',
            '}}',
            '</pre>',
        ]
        return "\n".join(html)

    def get_template_CONF_DOMESTIC_NO_REVIEW(self):
        html = [
            '<pre class="mb-0" >',
            '@article{{{citekey},',
            '  title = {{{title}}},',
            '  author = {{{authors}}},',
            '  journal = {{{book_title}}},',
            '  month = {{{month}}},',
            '  year = {{{year}}}},',
            '  note = {{{note}}},',
            '}}',
            '</pre>',
        ]
        return "\n".join(html)

    def get_template_NATIONAL(self):
        html = [
            '<pre class="mb-0" >',
            '@inproceedings{{{citekey},',
            '  title = {{{title}}},',
            '  author = {{{authors}}},',
            '  booktitle = {{{book_title}}},',
            '  month = {{{month}}},',
            '  year = {{{year}}},',
            '}}',
            '</pre>',
        ]
        return "\n".join(html)

    def get_template_BOOK(self):
        html = [
            '<pre class="mb-0" >',
            '@article{{{citekey},',
            '  title = {{{title}}},',
            '  author = {{{authors}}},',
            '  booktitle = {{{book_title}}},',
            '  pages = {{{page}}},',
            '  month = {{{month}}},',
            '  year = {{{year}}},',
            '}}',
            '</pre>',
        ]
        return "\n".join(html)

    def get_template_KEYNOTE(self):
        html = [
            '<pre class="mb-0" >',
            '@article{{{citekey},',
            '  title = {{{title}}},',
            '  author = {{{authors}}},',
            '  journal = {{{book_title}}},',
            '  month = {{{month}}},',
            '  year = {{{year}}},',
            '}}',
            '</pre>',
        ]
        return "\n".join(html)

    def get_template_NEWS(self):
        html = [
            '<pre class="mb-0" >',
            '@article{{{citekey},',
            '  title = {{{title}}},',
            '  author = {{{authors}}},',
            '  journal = {{{book_title}}},',
            '  month = {{{month}}},',
            '  year = {{{year}}},',
            '}}',
            '</pre>',
        ]
        return "\n".join(html)

    def get_template_OTHERS(self):
        html = [
            '<pre class="mb-0" >',
            '@article{{{citekey},',
            '  title = {{{title}}},',
            '  author = {{{authors}}},',
            '  journal = {{{book_title}}},',
            '  volume = {{{volume}}},',
            '  number = {{{number}}},',
            '  pages = {{{page}}},',
            '  month = {{{month}}},',
            '  year = {{{year}}},',
            '}}',
            '</pre>',
        ]
        return "\n".join(html)

    def get_template_AWARD(self):
        html = [
            '<pre class="mb-0" >',
            '@inproceedings{{{citekey},',
            '  title = {{{title}},',
            '  author = {{{authors}}},',
            '  booktitle = {{{book_title}}},',
            '  month = {{{month}},',
            '  year = {{{year}}},',
            '}}',
            '</pre>',
        ]
        return "\n".join(html)


# ===================
#  Custom Latex View
# ===================
class BibtexFormatLatexDefault(BibtexFormatBase):
    def get_template_DEFAULT(self):
        html = (
            '\item {authors}, '
            '"{title}", '
            '{book_title}, '
            '{volume}, {year},'
        )
        return html

# ----------------------------------------------------------------------------

# ===================
#  Filter Func.
# ===================
@register.filter(name='bibtex_list_format')
def bibtex_list_format(bibtex, func=BibtexFormatListDefault, *args,**kwargs):
    """
    Args.
    -----
    - bibtex: core.Bibtex object
    """
    return func(bibtex)()


@register.filter(name='bibtex_bib_format')
def bibtex_bib_format(bibtex, func=BibtexFormatBibtexDefault, *args,**kwargs):
    """
    Args.
    -----
    - bibtex: core.Bibtex object
    """
    return func(bibtex)()


@register.filter(name='bibtex_latex_format')
def bibtex_latex_format(bibtex, func=BibtexFormatLatexDefault, *args,**kwargs):
    """
    Args.
    -----
    - bibtex: core.Bibtex object
    """
    return func(bibtex)()
