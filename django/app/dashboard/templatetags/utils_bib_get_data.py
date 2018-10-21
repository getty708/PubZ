from django.shortcuts import reverse

from django import template
register = template.Library()

from core.models import Author, AuthorOrder, Tag

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
        tags = Tag.objects.filter(bibtex=bibtex).order_by('name')
        context["tags"] = self.get_string_tags(tags)

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