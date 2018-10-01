from django.shortcuts import reverse
from django.utils.safestring import mark_safe

from django import template
register = template.Library()



"""
Bibtex Format Filter
"""
# ==================
#  Custom List View
# ==================
def bibtex_format_callback_list_simple(bibtex, *args, **kwargs):
    title = bibtex.title_en if bibtex.title_en else bibtex.title_ja
    url_bib = reverse("dashboard:bib_detail", kwargs={'pk':bibtex.id})

    # Authors
    html_authors_base = """
    <a href="#">Author{}</a>
    """
    html_authors = [html_authors_base.format(i) for i in range(3)]
    html_authors = ", ".join(html_authors)
    
    html = """
    {authors}; <a href="{url_bib}">{title}</a>, 2017
    """.format(
        authors=html_authors, title=title, url_bib=url_bib
    )
    return mark_safe(html)




# ====================
#  Custom Bibtex View
# ====================
def bibtex_format_callback_bibtex_simple(bibtex):

    context = {
        'title': bibtex.title_en if bibtex.title_en else bibtex.title_ja,
        'authors': "Amagata, Daichi and Hara, Takahiro and Onizuka, Makoto",
        'book': str(bibtex.book),
        'vol': bibtex.volume,
        'number': bibtex.number,
        'pages': bibtex.page,
        'year': bibtex.pub_date.year,
        'publisher': bibtex.book.publisher,
    }
    
    html = [
        '<pre class="mb-0" >',
        '@article{{citekey,',
        '  title={title},',
        '  author={authors},',
        '  journal={book},',
        '  volume={vol},',
        '  number={number},',
        '  pages={pages},',
        '  year={year},',
        '  publisher={publisher},',
        '}}',
        '</pre>',
    ]
    html = "\n".join(html).format(**context)
    return mark_safe(html)



# ===================
#  Custom Latex View
# ===================
def bibtex_format_callback_latex_simple(bibtex):

    context = {
        'title': bibtex.title_en if bibtex.title_en else bibtex.title_ja,
        'authors': "Amagata, Daichi and Hara, Takahiro and Onizuka, Makoto",
        'book': str(bibtex.book),
        'vol': bibtex.volume,
        'number': bibtex.number,
        'pages': bibtex.page,
        'year': bibtex.pub_date.year,
        'publisher': bibtex.book.publisher,
    }
    
    html = '\item {authors}, "{title}", {book}, {vol}, {year},'
    html = html.format(**context)
    return mark_safe(html)





# ===================
#  Filter Func.
# ===================
@register.filter(name='bibtex_list_format')
def bibtex_list_format(bibtex, func=bibtex_format_callback_list_simple, *args,**kwargs):
    """
    Args.
    -----
    - bibtex: core.Bibtex object
    """
    return func(bibtex, *args, **kwargs)



@register.filter(name='bibtex_bib_format')
def bibtex_bib_format(bibtex, func=bibtex_format_callback_bibtex_simple, *args,**kwargs):
    """
    Args.
    -----
    - bibtex: core.Bibtex object
    """
    return func(bibtex)


@register.filter(name='bibtex_latex_format')
def bibtex_latex_format(bibtex, func=bibtex_format_callback_latex_simple, *args,**kwargs):
    """
    Args.
    -----
    - bibtex: core.Bibtex object
    """
    return func(bibtex)
