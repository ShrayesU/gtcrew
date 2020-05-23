from django.urls import path

from event.views import (
    EventListView, EventDetailView, ResultView, ResultDataTable, EventListViewPrivate, CreateEventViewPrivate,
    EventDetailViewPrivate, EventUpdateViewPrivate, EventDeleteViewPrivate, CreateResultViewPrivate,
    ResultDetailViewPrivate, ResultUpdateViewPrivate, ResultDeleteViewPrivate, view_leaderboard
)

app_name = 'event'

urlpatterns = [
    path('result/', ResultView.as_view(), name='result'),
    path('list/', EventListView.as_view(), name='list'),
    path('data/', ResultDataTable.as_view(), name='resultdatatable'),
    path('<int:pk>/view/', EventDetailView.as_view(), name="event_view"),
    # Private Member urls: Event
    path('member/list/', EventListViewPrivate.as_view(), name='member_event_list'),
    path('member/create/', CreateEventViewPrivate.as_view(), name='member_event_create'),
    path('member/<int:pk>/view/', EventDetailViewPrivate.as_view(), name='member_event_view'),
    path('member/<int:pk>/edit/', EventUpdateViewPrivate.as_view(), name='member_event_edit'),
    path('member/<int:pk>/delete/', EventDeleteViewPrivate.as_view(), name='member_event_delete'),
    # Private Member urls: Result
    # path('member/result/list/', ResultListViewPrivate.as_view(), name='member_result_list'),
    path('member/result/leaderboard/', view_leaderboard, name='member_result_leader_board'),
    path('member/result/create/', CreateResultViewPrivate.as_view(), name='member_result_create'),
    path('member/result/<int:pk>/view/', ResultDetailViewPrivate.as_view(), name='member_result_view'),
    path('member/result/<int:pk>/edit/', ResultUpdateViewPrivate.as_view(), name='member_result_edit'),
    path('member/result/<int:pk>/delete/', ResultDeleteViewPrivate.as_view(), name='member_result_delete'),
]
