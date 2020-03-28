from django.urls import path, include
from tastypie.api import Api

from team.api import ProfileResource
from . import views

v1_api = Api(api_name='v1')
v1_api.register(ProfileResource())

app_name = 'team'
urlpatterns = [
    path('', views.home_view, name='index'),
    path('<str:page_name>/', views.page_view, name='page'),
    path('team/membership/', views.IndexView.as_view(), name='member_index'),
    path('team/membership/<int:pk>/', views.DetailView.as_view(), name='member_detail'),
    path('form/interest/', views.interest, name='interest'),
    path('form/signup/', views.signup, name='signup'),
    path('team/api/', include(v1_api.urls)),
]
