from django.views.generic import ListView, DetailView, TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from event.models import Event, Result


class EventListView(ListView):
    model = Event
    context_object_name = "events"
    template_name = "event_list.html"


class EventDetailView(DetailView):
    model = Event
    context_object_name = "event_record"
    template_name = "view_event.html"


class ResultView(TemplateView):
    model = Result
    template_name = 'result.html'


class ResultDataTable(BaseDatatableView):
    model = Result
    columns = ['event.start_datetime.date()', 'event.name', 'name', 'squad.squad', 'time', 'distance']
