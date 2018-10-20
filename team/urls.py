from django.urls import path

from . import views

app_name = 'team'
urlpatterns = [
    path('', views.HomeView, name='index'),
    path('<str:pagename>/', views.PageView, name='page'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('signup/', views.signup, name='signup')
]
