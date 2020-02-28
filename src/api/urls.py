from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views as views_rest_auth

from api import views
from api import views_autocomplete
from api import views_cards
from api import views_rest


# -----------------------------------------------
router = routers.DefaultRouter()
router.register(r'users', views_rest.UserViewSet)
router.register(r'authors', views_rest.AuthorViewSet)
router.register(r'author-orders', views_rest.AuthorOrderViewSet)
router.register(r'books', views_rest.BookViewSet)
router.register(r'bibtexs', views_rest.BibtexViewSet)


# -----------------------------------------------
app_name = 'api'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),    
    path('cards/', views_cards.render_cards, name='render_cards'),
    path('autocomplete/author/', views_autocomplete.AutocompleteAuthor.as_view(), name='autocomplete_author'),
    path('autocomplete/book/', views_autocomplete.AutocompleteBook.as_view(), name='autocomplete_book'),

    # REST API
    path('rest/', include((router.urls,'api')),name="rest"),
    path('rest/api-token-auth/', views_rest_auth.obtain_auth_token, name="get_token"),
]
