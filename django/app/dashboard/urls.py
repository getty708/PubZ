from django.urls import path

from dashboard import views

app_name = 'dashboard'
urlpatterns = [
    # ex: /polls/
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
]
