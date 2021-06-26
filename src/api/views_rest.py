from api import serializers
from core.models import Author, AuthorOrder, Bibtex, Book
from rest_framework import filters, permissions, viewsets
from rest_framework.authentication import (
    BasicAuthentication,
    SessionAuthentication,
    TokenAuthentication,
)
from users.models import User


# -------------------------------------------------------------------
class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Instance must have an attribute named `owner`.
        return request.user.is_superuser


# User
# -------------------------------------------------------------------
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = serializers.UserSerializer
    # permission_classes = (IsAdminOrReadOnly,)
    authentication_classes = (
        SessionAuthentication,
        BasicAuthentication,
    )


# -------------------------------------------------------------------
class AuthorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Author.objects.all().order_by("name_en")
    serializer_class = serializers.AuthorSerializer
    permission_classes = (IsAdminOrReadOnly,)
    authentication_classes = (
        SessionAuthentication,
        TokenAuthentication,
    )
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name_en", "name_ja")


class AuthorOrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = AuthorOrder.objects.all().order_by("bibtex", "order")
    serializer_class = serializers.AuthorOrderSerializer
    permission_classes = (IsAdminOrReadOnly,)
    authentication_classes = (
        SessionAuthentication,
        TokenAuthentication,
    )


class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Book.objects.all().order_by("style", "title")
    serializer_class = serializers.BookSerializer
    permission_classes = (IsAdminOrReadOnly,)
    authentication_classes = (
        SessionAuthentication,
        TokenAuthentication,
    )
    filter_backends = (filters.SearchFilter,)
    search_fields = ("title",)


class BibtexViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Bibtex.objects.all().order_by(
        "title_en",
        "title_ja",
    )
    serializer_class = serializers.BibtexSerializer
    permission_classes = (IsAdminOrReadOnly,)
    authentication_classes = (
        SessionAuthentication,
        TokenAuthentication,
    )
    filter_backends = (filters.SearchFilter,)
    search_fields = ("title_en", "title_ja")
