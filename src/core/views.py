import urllib
from datetime import datetime

from core.models import Author, Bibtex, Book, Tag
from core.templatetags import utils_search as utils
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.urls import resolve
from django.utils.decorators import method_decorator
from django.views import generic

"""
Bibtex
"""


@method_decorator(login_required, name="dispatch")
class IndexView(generic.ListView):
    template_name = "dashboard/bibtex/index.html"
    context_object_name = "latest_bibtex_list"

    def get_queryset(self):
        self.GET_params = utils.parse_GET_params(self.request)
        query_set = utils.get_bibtex_query_set(self.GET_params).order_by(
            "book__style", "-pub_date"
        )
        self.GET_params["num_hits"] = len(query_set)
        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["GET_params"] = self.GET_params
        current_url_name = resolve(self.request.path_info).url_name
        if current_url_name != "index":
            context["display_style"] = current_url_name.split("_")[-1]
        context["year"] = datetime.now().year
        return context


class IndexViewPagination(generic.ListView):
    template_name = "dashboard/bibtex/index_page.html"
    context_object_name = "latest_bibtex_list"
    paginate_by = 30

    def get_paginate_by(self, queryset):
        """ Returns the number of items to paginate by, or None for no pagination. """
        if hasattr(self, "GET_params") and self.GET_params.get(
            "period_method", "ACADEMIC_YEAR"
        ) in ["ACADEMIC_YEAR", "YEAR"]:
            if (
                "period_year" in self.GET_params.keys()
                and self.GET_params.keys() is not None
            ):
                return 200
        return self.paginate_by

    def get_queryset(self):
        self.GET_params = utils.parse_GET_params(self.request)
        query_set = utils.get_bibtex_query_set(self.GET_params)
        self.GET_params["num_hits"] = len(query_set)
        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["GET_params"] = self.GET_params
        current_url_name = resolve(self.request.path_info).url_name
        if current_url_name != "index":
            context["display_style"] = current_url_name.split("_")[-1]
        return context


class DetailView(generic.DetailView):
    model = Bibtex
    template_name = "dashboard/bibtex/detail.html"


"""
Book
"""


class BookIndexView(generic.ListView):
    template_name = "dashboard/book/index.html"
    context_object_name = "latest_book_list"
    paginate_by = 30
    styles = utils.get_bib_style_keys()

    def get_queryset(self):
        self.selected_style = self.request.GET.get("style", "ALL")
        self.keywords = self.request.GET.get("keywords", "").split()
        styles = [s[0] for s in self.styles]
        key = self.selected_style if self.selected_style in styles else False
        queryset = Book.objects
        if key:
            queryset = queryset.filter(
                style=key,
            )
        if len(self.keywords):
            for q in self.keywords:
                queryset = queryset.filter(Q(title__icontains=q) | Q(abbr__icontains=q))
        return queryset.order_by("title")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        style_active = None
        for style in self.styles:
            if style[0] == self.selected_style:
                style_active = style[0]
                continue
        context["book_style"] = style_active  # context["style"][1]
        context["search_keywords"] = " ".join(self.keywords)
        return context


class BookDetailView(generic.DetailView):
    model = Book
    template_name = "dashboard/book/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest_bibtex_list"] = Bibtex.objects.filter(
            book=self.object
        ).order_by("-pub_date")[:20]
        return context


"""
Author
"""


class AuthorIndexView(generic.ListView):
    template_name = "dashboard/author/index.html"
    context_object_name = "latest_author_list"
    paginate_by = 30

    def get_queryset(self):
        self.search_keyword = self.request.GET.get(
            "keyword",
        )
        if self.search_keyword:
            queryset = Author.objects.order_by("name_en")
            self.search_keyword = urllib.parse.unquote(self.search_keyword).split()
            for q in self.search_keyword:
                queryset = queryset.filter(
                    Q(name_en__icontains=q)
                    | Q(name_ja__icontains=q)
                    | Q(affiliation_en__icontains=q)
                    | Q(affiliation_ja__icontains=q)
                )
            return queryset.order_by("name_en")
        return Author.objects.order_by("name_en")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_keyword"] = (
            " ".join(self.search_keyword)
            if isinstance(self.search_keyword, list)
            else ""
        )
        return context


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = "dashboard/author/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest_bibtex_list"] = Bibtex.objects.filter(
            authors=self.object
        ).order_by("-pub_date")[:20]
        return context


"""
Tag
"""


class TagIndexView(generic.ListView):
    template_name = "dashboard/tag/index.html"
    context_object_name = "latest_tag_list"

    def get_queryset(self):
        return Tag.objects.order_by("name")


class TagDetailView(generic.DetailView):
    model = Tag
    template_name = "dashboard/tag/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest_bibtex_list"] = Bibtex.objects.filter(
            tags=self.object
        ).order_by("-pub_date")[:20]
        return context
