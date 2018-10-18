from django.urls import path

from api import views
from api import views_autocomplete

app_name = 'api'
urlpatterns = [
    path('', views.index, name='index'),   
    path('autocomplete/author/', views_autocomplete.AutocompleteAuther.as_view(), name='autocomplete_author'),    
]
