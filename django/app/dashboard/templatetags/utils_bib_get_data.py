from django.shortcuts import reverse

from django import template
register = template.Library()

from core.models import Author, AuthorOrder, Tag, TagChain

class BibtexGetData(object):
    def __init__(self, bibtex, *args, **kwargs):
        self.bibtex = bibtex
        self.style = bibtex.book.style
        self.url_bib = reverse("dashboard:bib_detail", kwargs={'pk':bibtex.id})

    def __call__(self, type):
        # Convert Bibtex object into dict
        bibtex = self.bibtex
        context = bibtex.__dict__

        context['publisher'] = bibtex.book.publisher
        context["book_style"] = self.translate_book_style(self.style)

        # Get Authors
        authors = AuthorOrder.objects.filter(bibtex=bibtex).order_by('order')
        context["authors"] = self.get_string_authors(authors)

        # Get tags
        tags = TagChain.objects.filter(bibtex=bibtex).order_by('created')
        context["tags"] = self.get_string_tags(tags)
        #context["tags"] = "tagtest"

        return context[type]

    def translate_book_style(self, book_style):

        return book_style##koko

    def get_string_tags(self, tags):

        if len(tags) == 0:
            return "None"
        tags_string = ""
        for i, tag in enumerate(tags):
            tag = tag.tag.name
            tags_string += tag+","
        return tags_string

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


    def get_string_authors(self, authors):

        if len(authors) == 0:
            return "None"
        names_string = ""
        for i, author in enumerate(authors):
            name = self.get_author_name(author.author)
            names_string += name+","
        return names_string

@register.filter(name='bibtex_get')
def bibtex_get(bibtex, type):
    return BibtexGetData(bibtex)(type)

@register.filter(name='get_display_name')
def get_display_name(book_style):

    book_style_list = ["INTPROC","JOURNAL","CONF_DOMESTIC","CONF_DOMESTIC_NO_REVIEW","CONF_NATIONAL","BOOK","KEYNOTE","NEWS","OTHERS","AWARD"]
    display_name_list = ["Interproceedings","Journal Paper","Domestic Conference","Domestic Conference(NoReview)","National Conference","Book/Review/Editor/Translation","Presentaion/Panel Discution/Seminer	","News Paper article","others","Award"]

    return display_name_list[book_style_list.index(book_style)]

@register.filter(name='get_booktype_bibtex')
def get_booktype_bibtex(bibtex, book_style):
    return bibtex.filter(book__style=book_style)

@register.filter(name='get_booktype_book')
def get_booktype_book(book, book_style):
    return book.filter(style=book_style)
