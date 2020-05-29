# from django.contrib.auth.models import User, Group
import django
from django.http import  HttpResponseServerError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from users.models import User


# -------------------------------------------------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email',)


"""
User
"""
def get_login_user(user_id):
    return get_object_or_404(User, pk=user_id)

    

# -------------------------------------------------------------------
# ===========
#  My Models
# ===========
from core.models import Author, AuthorOrder, Bibtex, Book


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author        
        fields = (
            'id','name_en', 'name_ja',
            'affiliation_en', 'affiliation_ja',
            'mail', 'modified'
        )
        
    def create(self, validated_data):
        author  = Author.objects.create(**validated_data)
        author.owner = self.context['request'].user
        author.save()
        return author
    
        
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id','style','title','abbr','modified')

    def create(self, validated_data):
        book = Book.objects.create(**validated_data)
        book.owner = self.context['request'].user
        book.save()
        return book

        
class BibtexSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.IntegerField(max_value=None, min_value=None)
        
    class Meta:
        model = Bibtex
        fields = (
            'id','language',
            'pub_date','title_en', 'title_ja', 'bib_type',
            "volume","number","page", "pub_date",
            'book', "book_id", 'book_title',
            'url','fund',
            'modified',
            )

    def create(self, validated_data):
        book_id = validated_data.pop('book_id')
        book = get_object_or_404(Book, pk=book_id)
        
        try:
            bibtex = Bibtex.objects.create(book_id=book.id, **validated_data)
            bibtex.owner = self.context['request'].user
            bibtex.save()
        except django.db.u0tils.IntegrityError as e:
            raise serializers.ValidationError("DB IntegrityError: {}".format(e))
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
        try:
            author_order = AuthorOrder.objects.create(bibtex=bib,author=author,**validated_data)
            author_order.owner = self.context['request'].user
            author_order.save()
        except django.db.utils.IntegrityError:
            raise serializers.ValidationError("DB IntegrityError")
        return author_order
        



        
