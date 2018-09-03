from django.urls import path

from dashboard import views, views_man

app_name = 'dashboard'
urlpatterns = [
    # ex: /polls/
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('manage/', views_man.IndexView.as_view(), name='management'),
]
