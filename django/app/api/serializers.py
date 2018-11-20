# from django.contrib.auth.models import User, Group
from users.models import User
from rest_framework import serializers
from django.shortcuts import get_object_or_404




# -------------------------------------------------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email',)



# -------------------------------------------------------------------
# ===========
#  My Models
# ===========
from core.models import Author, AuthorOrder, Bibtex, Book


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author        
        fields = ('id','name_en', 'name_ja', 'dep_en', 'dep_ja','modified')

        
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id','style','title','abbr','modified')

        
class BibtexSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=False)
    
    class Meta:
        model = Bibtex
        fields = (
            'id','language',
            'pub_date','title_en', 'title_ja',
            "volume","number","page", "pub_date",
            'book','modified'
            )

    def create(self, validated_data):
        book = validated_data.pop('book')
        book = Book.objects.filter(title=book["title"])
        if len(book) > 0:
            bibtex = Bibtex.objects.create(book=book[0], **validated_data)        
        else:
            bibtex =  Bibtex.objects.create(**validated_data)
        return bibtex

        
class AuthorOrderSerializer(serializers.ModelSerializer):
    bibtex = BibtexSerializer()
    author = AuthorSerializer()
    
    class Meta:
        model = AuthorOrder
        fields = ('id','bibtex','author','order','modified')

    def create(self, validated_data):
        # Bib
        bib = validated_data.pop('bibtex')
        if bib["language"] == "EN":
            bib = Bibtex.objects.filter(title_en=bib["title_en"])
        else:
            bib = Bibtex.objects.filter(title_ja=bib["title_ja"])

        # Author
        author = validated_data.pop('author')
        author = Author.objects.filter(name_en=author["name_en"])
        if len(author) == 0:
            author = Auhtor.objects.filter(name_ja=author["name_ja"])                    
        if len(bib) > 0 and len(author) > 0:
            author_order = AuthorOrder.objects.create(
                bibtex=bib[0],author=author[0],**validated_data)        
        else:
            author_order =  AuthorOrder.objects.create(**validated_data)
        return author_order
        



        
