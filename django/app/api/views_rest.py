from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions, filters


# Import Serializers
from api import serializers

# Import models
from core.models import Author, AuthorOrder, Bibtex, Book
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication

# User
# ------------------------------------------------------------------- 
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = serializers.UserSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication,)    


# -------------------------------------------------------------------
class AuthorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Author.objects.all().order_by('name_en')
    serializer_class = serializers.AuthorSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (SessionAuthentication,TokenAuthentication,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name_en','name_ja',)

    
class AuthorOrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = AuthorOrder.objects.all().order_by('bibtex','order')
    serializer_class = serializers.AuthorOrderSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (SessionAuthentication, TokenAuthentication,)


class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Book.objects.all().order_by('style', 'title')
    serializer_class = serializers.BookSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title',)
    

class BibtexViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Bibtex.objects.all().order_by('title_en','title_ja',)
    serializer_class = serializers.BibtexSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title_en','title_ja')
    
    
