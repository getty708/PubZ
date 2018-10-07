from django.contrib import admin

# Register your models here.
from core.models import Author, Bibtex, Book, Tag, AuthorOrder


# ---------------------------
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id','name_en', 'dep_en', 'created', 'modified', 'owner')
    list_display_links = ('name_en',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id','style','title','abbr','created','modified','owner')
    list_display_links = ('title','abbr')
    


@admin.register(Bibtex)
class BibtexAdmin(admin.ModelAdmin):
    list_display = ('id','pub_date','get_title','book','created','modified','owner')
    list_display_links = ('get_title',)

    def get_title(self, obj):
        if obj.language == 'EN':
            return obj.title_en
        elif obj.language == 'JA':
            return obj.title_en
        return "Bibtex[{}]".format(obj.id)
    get_title.short_description = 'Title'
        
    

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(AuthorOrder)
class AuthorOrderAdmin(admin.ModelAdmin):
    list_display = ('id','bibtex','author','order',)
    list_display_links = ('bibtex','author',)
    
