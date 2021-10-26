from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import pgettext_lazy
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, FieldRowPanel, InlinePanel as BaseInlinePanel, \
    HelpPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page, Orderable
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet
from wagtailautocomplete.edit_handlers import AutocompletePanel

from event.utils import EVENT_TYPES, RACE
from team.utils import RACER


class InlinePanel(BaseInlinePanel):
    # TODO: remove this after wagtail fixes Choosers in nested inlines
    def widget_overrides(self):
        widgets = {}
        child_edit_handler = self.get_child_edit_handler()
        for handler_class in child_edit_handler.children:
            widgets.update(handler_class.widget_overrides())
        widget_overrides = {self.relation_name: widgets}
        return widget_overrides


class Racer(Orderable):
    page = ParentalKey("event.Result", related_name="racers")
    person_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='results_raced',  # TODO: use results_raced or switch back to +
        help_text='You can only search for a Published person page. '
                  '"Create New" only works if you have Publish permissions.'
    )
    position = models.ForeignKey(
        'team.Title',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='+',
        limit_choices_to={'held_by': RACER},
    )

    def __str__(self):
        if self.person_page:
            return '%s %s' % (self.person_page.specific.first_name, self.person_page.specific.last_name)
        else:
            return ''

    panels = [
        AutocompletePanel('person_page', 'person.PersonPage'),
        SnippetChooserPanel('position'),
    ]


class BaseResult(models.Model):
    date = models.DateField(null=True, blank=True)
    squad = models.ForeignKey(
        'team.Squad',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='+',
    )
    distance = models.PositiveIntegerField(help_text='meters')
    minutes = models.PositiveIntegerField(default=0)
    seconds = models.DecimalField(max_digits=5, decimal_places=3, default=0,
                                  validators=[MinValueValidator(0), MaxValueValidator(59.999)])
    lightweight = models.BooleanField(default=False)
    pace = models.FloatField(default=0, editable=False)

    result_panels = [
        FieldPanel('date'),
        MultiFieldPanel([
            FieldRowPanel([
                SnippetChooserPanel('squad', classname="col6"),
                FieldPanel('lightweight', classname="col6"),
            ])
        ], heading="Squad"),
        FieldPanel('distance'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('minutes', classname="col6"),
                FieldPanel('seconds', classname="col6"),
            ])
        ], heading="Time"),
    ]

    class Meta:
        abstract = True

    def clean(self):
        super().clean()
        self.pace = self.get_pace()

    @property
    def total_time_string(self):
        """Returns string of total time"""
        return '{:02d}:{:06.3f}'.format(self.minutes, self.seconds)

    def get_pace(self):
        """Returns the pace rowed in the form of seconds per 500 meters."""
        seconds = float(self.minutes * 60) + float(self.seconds)
        five_hundred = float(self.distance) / 500
        return seconds / five_hundred

    @property
    def pace_string(self):
        """Returns pace in string format of MM:SS.mmm/Meters"""
        pace = self.get_pace()
        minutes, seconds = int(pace // 60), pace % 60
        return '{:02d}:{:06.3f}/500m'.format(minutes, seconds)

    def watts(self):
        """Returns the power in watts based on average pace per 500 meters."""
        pace = self.get_pace()
        return 2.80 / (pace ** 3)


class Result(BaseResult, ClusterableModel):
    page = ParentalKey("event.EventPage", related_name="results")
    entry = models.CharField(max_length=64, help_text='E.g. "Lightweight Varsity 8+"')
    rank = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), ])
    # TODO: add boat choosers

    panels = [
        FieldPanel('entry'),
        FieldPanel('rank'),
        HelpPanel('Make sure to "Save Draft" on new Results <strong>before</strong> adding Racers',
                  heading='Racers', classname='help-warning'),
        InlinePanel("racers", label="Racer"),
    ]
    panels[2:2] = BaseResult.result_panels  # insert the base result panels before inline racers


@register_snippet
class Regatta(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    @classmethod
    def autocomplete_create(cls: type, value: str):
        return cls.objects.create(title=value)


class EventPage(Page):
    location = models.CharField(pgettext_lazy('Location of Event', 'Location'), max_length=64)
    regatta = models.ForeignKey(
        'event.Regatta',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='+',
    )
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(blank=True, null=True)
    event_type = models.CharField(pgettext_lazy('Type of Event', 'Type'),
                                  max_length=64, choices=EVENT_TYPES, default=RACE)
    description = RichTextField(blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('location'),
        AutocompletePanel('regatta'),
        FieldPanel('event_type'),
        FieldPanel('description'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('start_datetime', classname="col6"),
                FieldPanel('end_datetime', classname="col6"),
            ])
        ], heading="Time"),
        MultiFieldPanel(
            [InlinePanel("results", label="Result")],
            heading="Results", classname="collapsible"
        ),
    ]

    parent_page_types = ['EventIndexPage']
    subpage_types = []

    def get_results(self):
        return self.results.all()

    def get_context(self, request, *args, **kwargs):
        context = super(EventPage, self).get_context(request)

        results = self.get_results()
        context['results'] = results

        return context


class EventIndexPage(Page):
    subpage_types = ['EventPage']
    max_count = 1

    def get_events(self):
        return EventPage.objects.live().descendant_of(
            self).order_by('-start_datetime')

    def get_context(self, request, *args, **kwargs):
        context = super(EventIndexPage, self).get_context(request)

        events = self.get_events()
        api_event = []
        for event in events:
            prepared = {'title': event.title,
                        'url': event.url,
                        'start': timezone.localtime(event.start_datetime).strftime("%Y-%m-%dT%H:%M:%S"), }
            if event.end_datetime:
                prepared.update({'end': timezone.localtime(event.end_datetime).strftime("%Y-%m-%dT%H:%M:%S"), })
            api_event.append(prepared)
        context.update({'api_event': api_event})

        context['events'] = events

        return context
