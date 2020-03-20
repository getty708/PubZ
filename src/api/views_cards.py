from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import generic

from core.models import Author, Bibtex, Book, TagChain, Tag
from core.templatetags import utils_search as utils

def render_cards(request):
    bibtex,query_param_dic = utils.perse_get_query_params(request)
    
    bib_to_render = []
    author_to_render = []

    for bib in bibtex:
        bib_to_render.append(bib)
        authors = bib.authors_list
        num_of_authors = len(authors)
        author_str = ''
        for i in range(num_of_authors):
            if i == (num_of_authors - 1):
                author_str += 'and {}'.format(authors[i]['name'])
            else:
                author_str += '{}, '.format(authors[i]['name'])
        author_to_render.append(author_str)
    
    tags = Tag.objects.all()
    defaul_img_path = '/media/default.png'

    return render(request,
                  'cards/cards_to_show.html',
                  {'papers_to_show': zip(bib_to_render, author_to_render),
                   'all_tags': tags,
                   'default_img': defaul_img_path})
