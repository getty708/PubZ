from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views import generic



from core.models import Author, Bibtex, Book


"""
Bibtex
"""
class IndexView(generic.ListView):
    template_name = 'dashboard/index.html'
    context_object_name = 'latest_bibtex_list'

    def get_queryset(self):
        #return Bibtex.objects.order_by('-pub_date').filter('style=='+book_style)[:5]
        return Bibtex.objects.order_by('-pub_date')[:5]


class IndexViewTable(generic.ListView):
    template_name = 'dashboard/bibtex/index_tab.html'
    context_object_name = 'latest_bibtex_list'

    def get_queryset(self):
        return Bibtex.objects.order_by('-pub_date')[:5]


class IndexViewBib(generic.ListView):
    template_name = 'dashboard/bibtex/index_bib.html'
    context_object_name = 'latest_bibtex_list'

    def get_queryset(self):
        return Bibtex.objects.order_by('-pub_date')[:5]

class IndexViewLatex(generic.ListView):
    template_name = 'dashboard/bibtex/index_latex.html'
    context_object_name = 'latest_bibtex_list'

    def get_queryset(self):
        return Bibtex.objects.order_by('-pub_date')[:5]



class DetailView(generic.DetailView):
    model = Bibtex
    template_name = 'dashboard/detail.html'



"""
Book
"""
class BookIndexView(generic.ListView):
    template_name = 'dashboard/book/index.html'
    context_object_name = 'latest_book_list'

    def get_queryset(self):
        return Book.objects.order_by('title')


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'dashboard/book/detail.html'




"""
Author
"""
class AuthorIndexView(generic.ListView):
    template_name = 'dashboard/author/index.html'
    context_object_name = 'latest_author_list'

    def get_queryset(self):
        return Author.objects.order_by('name_en')


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'dashboard/author/detail.html'
