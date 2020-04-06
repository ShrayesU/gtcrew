from django.urls import path, include
from tastypie.api import Api

from team.api import ProfileResource
from . import views

v1_api = Api(api_name='v1')
v1_api.register(ProfileResource())

app_name = 'team'
urlpatterns = [
    path('', views.home_view, name='index'),
    path('page/<str:page_name>/', views.page_view, name='page'),
    path('team/membership/', views.IndexView.as_view(), name='member_index'),
    path('team/membership/<int:pk>/', views.DetailView.as_view(), name='member_detail'),
    path('form/interest/', views.interest, name='interest'),
    path('member/register/', views.signup, name='register'),
    path('team/api/', include(v1_api.urls)),
    # Profile urls
    path('member/profile/list/', views.ProfileListView.as_view(), name='list_profile'),
    path('member/profile/create/', views.CreateProfileView.as_view(), name='create_profile'),
    path('member/profile/<int:pk>/view/', views.ProfileDetailView.as_view(), name='view_profile'),
    path('member/profile/<int:pk>/edit/', views.ProfileUpdateView.as_view(), name='edit_profile'),
    path('member/profile/<int:profile_id>/manage_memberships/', views.manage_memberships, name='manage_memberships'),
    path('member/profile/<int:profile_id>/manage_awards/', views.manage_awards, name='manage_awards'),
    # Membership urls
    path('member/membership/list/', views.MembershipListView.as_view(), name='list_membership'),
    path('member/membership/create/', views.CreateMembershipView.as_view(), name='create_membership'),
    path('member/membership/<int:pk>/view/', views.MembershipDetailView.as_view(), name='view_membership'),
    path('member/membership/<int:pk>/edit/', views.MembershipUpdateView.as_view(), name='edit_membership'),
    # Award urls
    path('member/award/list/', views.AwardListView.as_view(), name='list_award'),
    path('member/award/<int:pk>/view/', views.AwardDetailView.as_view(), name='view_award'),
    path('member/award/given/<int:pk>/view/', views.AwardGivenDetailView.as_view(), name='view_awardgiven'),
]
