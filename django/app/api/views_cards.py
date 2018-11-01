from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import generic

from core.models import Author, Bibtex, Book, TagChain, Tag

def render_cards(request):
    if 'team' in request.GET:
        team = request.GET.get('team')
    query = sorted(request.GET.values())
    print(query)

    bibtex = Bibtex.objects.order_by('-pub_date')
    bib_to_render = []
    author_to_render = []
    for bib in bibtex:
        if bib.tags.all()[0].name == team:
            bib_to_render.append(bib)
            authors = bib.authors.all()
            num_of_authors = len(bib.authors.all())
            author_str = ''
            for i in range(num_of_authors):
                if i == (num_of_authors - 1):
                    author_str += 'and {}'.format(authors[i])
                else:
                    author_str += '{}, '.format(authors[i])
            author_to_render.append(author_str)


    return render(request,
                  'cards/cards_to_show.html',
                  {'papers_to_show': zip(bib_to_render, author_to_render)})