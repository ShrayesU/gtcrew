from django.urls import path

from . import views

app_name = 'team'
urlpatterns = [
    # Member urls
    path('member/', views.PortalView.as_view(), name='index_member'),
    # Profile urls
    path('member/profile/list/', views.ProfileListView.as_view(), name='list_profile'),
    path('member/profile/list/search/', views.SearchProfileListView.as_view(), name='search_profile'),
    path('member/profile/autocomplete/', views.ProfileAutocomplete.as_view(), name='profile_autocomplete'),
    path('member/profile/create/', views.CreateProfileView.as_view(), name='create_profile'),
    path('member/profile/<int:pk>/view/', views.ProfileDetailView.as_view(), name='view_profile'),
    path('member/profile/<int:pk>/edit/', views.ProfileUpdateView.as_view(), name='edit_profile'),
    path('member/profile/<int:pk>/claim/', views.claim_profile, name='claim_profile'),
    path('member/profile/<int:profile_id>/manage_memberships/', views.manage_memberships, name='manage_memberships'),
    # Membership urls
    path('member/membership/list/', views.MembershipListView.as_view(), name='list_membership'),
    path('member/membership/create/', views.CreateMembershipView.as_view(), name='create_membership'),
    path('member/membership/<int:pk>/view/', views.MembershipDetailView.as_view(), name='view_membership'),
    path('member/membership/<int:pk>/edit/', views.MembershipUpdateView.as_view(), name='edit_membership'),
]
