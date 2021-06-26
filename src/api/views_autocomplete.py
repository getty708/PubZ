from core.models import Author, Book
from dal import autocomplete
from django.db.models import Q


class AutocompleteAuthor(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Author.objects.none()

        qs = Author.objects.all()
        if self.q:
            qs = qs.filter(Q(name_en__icontains=self.q) | Q(name_ja__icontains=self.q))
        return qs


class AutocompleteBook(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Book.objects.none()

        qs = Book.objects.all()
        if self.q:
            qs = qs.filter(Q(title__icontains=self.q) | Q(abbr__istartswith=self.q))
        return qs
