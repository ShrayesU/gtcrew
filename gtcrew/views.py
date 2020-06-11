from django.utils.encoding import force_str
from wagtail.admin.views.reports import PageReportView

from roster.models import TermPage


def person_page_to_string(value):
    value = [str(x) for x in value]
    return force_str(";".join(value))


class PeopleReportView(PageReportView):
    header_icon = 'users'
    template_name = 'reports/people_report.html'
    title = "People list by Term"

    custom_field_preprocess = {
        'coaches.all': {'xlsx': person_page_to_string, 'csv': person_page_to_string},
        'officers.all': {'xlsx': person_page_to_string, 'csv': person_page_to_string},
        'members.all': {'xlsx': person_page_to_string, 'csv': person_page_to_string},
    }

    list_export = PageReportView.list_export + ['start_date', 'coaches.all', 'officers.all',
                                                'members.all']
    export_headings = {
        'coaches.all': 'Coaches',
        'officers.all': 'Officers',
        'members.all': 'Members',
        **PageReportView.export_headings,
    }

    def get_queryset(self):
        return TermPage.objects.all()
