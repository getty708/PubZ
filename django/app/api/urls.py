from django.urls import path

from api import views
from api import views_cards
from api import views_autocomplete

app_name = 'api'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),    
    path('cards/', views_cards.render_cards, name='render_cards'),
    path('autocomplete/author/', views_autocomplete.AutocompleteAuthor.as_view(), name='autocomplete_author'),
    path('autocomplete/book/', views_autocomplete.AutocompleteBook.as_view(), name='autocomplete_book'),
]