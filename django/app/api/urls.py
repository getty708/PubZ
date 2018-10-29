from django.urls import path

from api import views, views_autocomplete

app_name = 'api'
urlpatterns = [
    path('', views.index, name='index'),   
    path('autocomplete/author/', views_autocomplete.AutocompleteAuthor.as_view(), name='autocomplete_author'),
    path('autocomplete/book/', views_autocomplete.AutocompleteBook.as_view(), name='autocomplete_book'),    
]
