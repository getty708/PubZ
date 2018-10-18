from dal import autocomplete

from core.models import Author


class AutocompleteAuther(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
#        if not self.request.user.is_authenticated():
#        	return Author.objects.none()

        qs = Author.objects.all()

        if self.q:
        	qs = qs.filter(name_en__istartswith=self.q)
        print(qs)

        return qs
