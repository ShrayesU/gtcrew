from django.urls import path
from asset.views import (
    AssetListView, CreateAssetView, AssetDetailView,
    AssetUpdateView, AssetDeleteView,
)

app_name = 'asset'

urlpatterns = [
    path('list/', AssetListView.as_view(), name='list'),
    path('create/', CreateAssetView.as_view(), name='create'),
    path('<int:pk>/view/', AssetDetailView.as_view(), name='view'),
    path('<int:pk>/edit/', AssetUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', AssetDeleteView.as_view(), name='delete'),
]
