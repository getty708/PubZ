# Register your models here.
from core.models import Author, AuthorOrder, Bibtex, Book, Tag, TagChain
from django.contrib import admin


# ---------------------------
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id", "name_en", "affiliation_en", "created", "modified", "owner")
    list_display_links = ("name_en",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "style", "title", "abbr", "created", "modified", "owner")
    list_display_links = ("title", "abbr")


@admin.register(Bibtex)
class BibtexAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "pub_date",
        "get_title",
        "book",
        "bib_type",
        "created",
        "modified",
        "owner",
    )
    list_display_links = (
        "id",
        "get_title",
    )

    def get_title(self, obj):
        if obj.title is not None:
            return obj.title
        return "Bibtex[{}]".format(obj.id)

    get_title.short_description = "Title"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "parent", "created")
    list_display_links = ("name",)


@admin.register(AuthorOrder)
class AuthorOrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "bibtex",
        "author",
        "order",
    )
    list_display_links = (
        "bibtex",
        "author",
    )


@admin.register(TagChain)
class TagChainAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "tag",
        "bibtex",
        "created",
    )
    list_display_links = (
        "tag",
        "bibtex",
    )
