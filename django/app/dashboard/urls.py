from django.urls import path

from dashboard import views, views_edit

app_name = 'dashboard'
urlpatterns = [
    # ex: /polls/
    path('', views.IndexView.as_view(), name='index'),
    path('list/', views.IndexView.as_view(), name='index_list'),
    path('tab/', views.IndexViewTable.as_view(), name='index_table'),
    path('bib/', views.IndexViewBib.as_view(), name='index_bib'),
    path('latex/', views.IndexViewLatex.as_view(), name='index_latex'),
    path('<int:pk>/', views.DetailView.as_view(), name='bib_detail'),
    path('bib/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('book/',          views.BookIndexView.as_view(),  name='book_index'),    
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('author/',         views.AuthorIndexView.as_view(),  name='author_index'),
    path('author/<int:pk>/',views.AuthorDetailView.as_view(), name='author_detail'),
    

    # Edit Function
    path('add',            views_edit.bibtex_edit, name='bibtex_add'),    
    path('edit/<int:pk>/', views_edit.bibtex_edit, name='bibtex_edit'),
    path('book/add',            views_edit.book_edit, name='book_add'),
    path('book/edit/<int:pk>/', views_edit.book_edit, name='book_edit'),    
    path('author/add',            views_edit.author_edit, name='author_add'),
    path('author/edit/<int:pk>/', views_edit.author_edit, name='author_edit'),
]
