from django.views.generic import ListView, DetailView
from event.models import Event


class EventListView(ListView):
    model = Event
    context_object_name = "events"
    template_name = "event_list.html"

class EventDetailView(DetailView):
    model = Event
    context_object_name = "event_record"
    template_name = "view_event.html"

