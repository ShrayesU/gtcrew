from django.urls import path
from event.views import (
    EventListView, EventDetailView,  ResultView, ResultDataTable
    #CreateEventView, UpdateEventView,
    #DeleteEventView, GetContactView, GetEventsView,
    #DeleteAttachmentView, AddAttachmentView
    )


app_name = 'event'


urlpatterns = [
    path('result/', ResultView.as_view(), name='result'),
    path('list/', EventListView.as_view(), name='list'),
    path('data/', ResultDataTable.as_view(), name='resultdatatable'),
    #path('create/', CreateEventView.as_view(), name='save'),
    path('<int:pk>/view/', EventDetailView.as_view(), name="event_view"),
    #path('<int:pk>/edit/', UpdateEventView.as_view(), name="event_edit"),
    #path('<int:pk>/delete/', DeleteEventView.as_view(), name="event_remove"),

    #path('contacts/', GetContactView.as_view(), name="contacts"),
    #path('get/list/', GetEventsView.as_view(), name="get_Event"),

    #path('attachment/add/', AddAttachmentView.as_view(), name="add_attachment"),
    #path('attachment/remove/', DeleteAttachmentView.as_view(), name="remove_attachment"),
]
