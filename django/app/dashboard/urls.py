from django.urls import include, path

from dashboard import views, views_edit

app_name = 'dashboard'
urlpatterns = [
    # ex: /polls/
    path('', views.IndexViewList.as_view(), name='index'),
    path('list/', views.IndexViewList.as_view(), name='index_list'),
    path('tab/', views.IndexViewTable.as_view(), name='index_table'),
    path('bib/', views.IndexViewBib.as_view(), name='index_bib'),
    path('latex/', views.IndexViewLatex.as_view(), name='index_latex'),
    path('<int:pk>/', views.DetailView.as_view(), name='bib_detail'),
    path('bib/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('book/',          views.BookIndexView.as_view(),  name='book_index'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('author/',         views.AuthorIndexView.as_view(),  name='author_index'),
    path('author/<int:pk>/',views.AuthorDetailView.as_view(), name='author_detail'),
    path('notification/alert',views.notification_alert,  name='notification_alert'),

    # email alert
    path('notification/alert/<str:author_id>/<int:bibtex_id>', views.notification_alert_author, name='alert_by_author'),
    path('notification/alert_all', views.notification_alert_all, name='alert_all'),

    path('tag/', views.TagIndexView.as_view(), name='tag_index'),
    path('tag/<int:pk>', views.TagDetailView.as_view(), name='tag_detail'),

    # Edit Function
    path('add',            views_edit.bibtex_edit, name='bibtex_add'),
    path('add/step1/',     views_edit.bibtex_edit_step1, name='bibtex_add_step1'),
    path('edit/<int:bibtex_id>/', views_edit.bibtex_edit, name='bibtex_edit'),
    path('book/add',            views_edit.book_edit, name='book_add'),
    path('book/edit/<int:book_id>/', views_edit.book_edit, name='book_edit'),
    path('author/add',
         views_edit.author_edit, name='author_add'),
    path('author/edit/<int:author_id>/',
         views_edit.author_edit, name='author_edit'),
    path('author/order/add',
         views_edit.author_order_edit, name='author_order_add'),
    path('author/order/edit/<int:author_order_id>/',
         views_edit.author_order_edit, name='author_order_edit'),
    path('tag/add',
         views_edit.tag_edit, name='tag_add'),
    path('tag/edit/<int:tag_id>/',
         views_edit.tag_edit, name='tag_edit'),
    path('tag/tagchain/add',
         views_edit.tagchain_edit, name='tagchain_add'),
    path('tag/tagchain/edit/<int:tagchain_id>/',
         views_edit.tagchain_edit, name='tagchain_edit')

]
