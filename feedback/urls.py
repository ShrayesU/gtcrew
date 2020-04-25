from django.urls import path

from .views import feedback_submission

app_name = 'feedback'
urlpatterns = [
    path('create/', feedback_submission, name='create'),
]
