from django.urls import path

from . import views

app_name = 'team'
urlpatterns = [
    path('', views.HomeView, name='index'),
    path('<str:pagename>/', views.PageView, name='page'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('form/interest/', views.interest, name='interest'),
    path('form/signup/', views.signup, name='signup'),
]
