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
        fields = ('id','name_en', 'name_ja', 'dep_en', 'dep_ja', 'mail', 'modified')

        
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id','style','title','abbr','modified')

        
class BibtexSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.IntegerField(max_value=None, min_value=None)
    
    class Meta:
        model = Bibtex
        fields = (
            'id','language',
            'pub_date','title_en', 'title_ja',
            "volume","number","page", "pub_date",
            'book','modified',"book_id",
            'url','note',
            )

    def create(self, validated_data):
        print(validated_data)
        book_id = validated_data.pop('book_id')
        book = Book.objects.filter(pk=book_id)
        if len(book) > 0:
            bibtex = Bibtex.objects.create(book_id=book[0].id, **validated_data)
        else:            
            bibtex =  Bibtex.objects.create(**validated_data)
        return bibtex

        
class AuthorOrderSerializer(serializers.ModelSerializer):
    bibtex = BibtexSerializer(read_only=True)
    author = AuthorSerializer(read_only=True)
    bibtex_id = serializers.IntegerField(max_value=None, min_value=None)
    author_id = serializers.IntegerField(max_value=None, min_value=None)
    
    class Meta:
        model = AuthorOrder
        fields = ('id','bibtex','author','order','modified','bibtex_id','author_id',)

        
    def create(self, validated_data):
        # Bib
        bib_id = validated_data.pop('bibtex_id')
        bib = get_object_or_404(Bibtex, pk=bib_id)
        # Author
        author_id = validated_data.pop('author_id')
        author    = get_object_or_404(Author, pk=author_id)

        # Create New 
        author_order = AuthorOrder.objects.create(
            bibtex=bib,author=author,**validated_data)
        return author_order
        



        
