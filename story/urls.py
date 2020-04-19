from django.urls import path
from story.views import (
    StoryListView, CreateStoryView, StoryDetailView,
    StoryUpdateView, StoryDeleteView,
)

app_name = 'story'

urlpatterns = [
    path('list/', StoryListView.as_view(), name='list'),
    path('create/', CreateStoryView.as_view(), name='create'),
    path('<slug:slug>/view/', StoryDetailView.as_view(), name='view'),
    path('<slug:slug>/edit/', StoryUpdateView.as_view(), name='edit'),
    path('<slug:slug>/delete/', StoryDeleteView.as_view(), name='delete'),
]
