from cuser.middleware import CuserMiddleware
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import pgettext_lazy
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, FieldRowPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from asset.models import Asset
from asset.utils import SHELL
from event.utils import EVENT_TYPES, RACE
from team.models import Squad, Profile


class ResultPage(Page):
    date = models.DateField(null=True, blank=True)
    entry = models.CharField(max_length=64, help_text='E.g. "Lightweight Varsity 8+"')
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
    rank = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), ])
    pace = models.FloatField(default=0, editable=False)
    # TODO: add rowers, coxswain, and boat choosers

    content_panels = Page.content_panels + [
        FieldPanel('entry'),
        FieldPanel('date'),
        SnippetChooserPanel('squad'),
        FieldPanel('distance'),
        FieldPanel('lightweight'),
        FieldPanel('rank'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('minutes', classname="col6"),
                FieldPanel('seconds', classname="col6"),
            ])
        ], heading="Time"),
    ]

    parent_page_types = ['EventPage']
    subpage_types = []

    def clean(self):
        super(ResultPage, self).clean()
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


@register_snippet
class Regatta(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


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
        SnippetChooserPanel('regatta'),
        FieldPanel('event_type'),
        FieldPanel('description'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('start_datetime', classname="col6"),
                FieldPanel('end_datetime', classname="col6"),
            ])
        ], heading="Time"),
    ]

    parent_page_types = ['EventIndexPage']
    subpage_types = ['ResultPage']

    def get_results(self):
        return ResultPage.objects.live().descendant_of(
            self).order_by('pace')

    def paginate(self, request, *args):
        page = request.GET.get('page')
        paginator = Paginator(self.get_results(), 12)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        return pages

    # Returns the above to the get_context method that is used to populate the
    # template
    def get_context(self, request, *args, **kwargs):
        context = super(EventPage, self).get_context(request)

        # ResultPage objects (get_results) are passed through pagination
        results = self.paginate(request, self.get_results())

        context['results'] = results

        return context


class EventIndexPage(Page):
    subpage_types = ['EventPage']

    def get_events(self):
        return EventPage.objects.live().descendant_of(
            self).order_by('-start_datetime')

    def paginate(self, request, *args):
        page = request.GET.get('page')
        paginator = Paginator(self.get_events(), 12)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        return pages

    # Returns the above to the get_context method that is used to populate the
    # template
    def get_context(self, request, *args, **kwargs):
        context = super(EventIndexPage, self).get_context(request)

        events = self.get_events()
        api_event = []
        for event in events:
            prepared = {'title': event.title,
                        'url': event.url,
                        'start': event.start_datetime.strftime("%Y-%m-%dT%H:%M:%S"), }
            if event.end_datetime:
                prepared.update({'end': event.end_datetime.strftime("%Y-%m-%dT%H:%M:%S"), })
            api_event.append(prepared)
        context.update({'api_event': api_event})

        # # EventPage objects (get_events) are passed through pagination
        # events = self.paginate(request, self.get_events())

        context['events'] = events

        return context


class Event(models.Model):
    name = models.CharField(pgettext_lazy('Name of Event', 'Name'), max_length=64)
    location = models.CharField(pgettext_lazy('Location of Event', 'Location'), max_length=64)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(blank=True, null=True)
    event_type = models.CharField(pgettext_lazy('Type of Event', 'Type'), max_length=64, choices=EVENT_TYPES)
    squads = models.ManyToManyField(Squad, blank=True)
    description = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    public = models.BooleanField(default=False)

    created_by = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        related_name='events_created',
        null=True, blank=True,
    )
    last_modified_by = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        related_name='events_last_modified',
        null=True, blank=True,
    )

    class Meta:
        ordering = ['start_datetime']

    def __str__(self):
        return '%s %s' % (self.name, self.start_datetime.year)

    def save(self, *args, **kwargs):
        user = CuserMiddleware.get_user()

        if user.is_staff:
            self.public = True
        else:
            self.public = False

        if not self.pk:
            self.created_by = user.profile
        self.last_modified_by = user.profile

        super(Event, self).save(*args, **kwargs)

    @property
    def start_date_string(self):
        """Returns string of start date"""
        return self.start_datetime.strftime("%Y-%m-%d")

    @property
    def absolute_url(self):
        return reverse_lazy('event:member_event_view', kwargs={'pk': self.pk})


class Result(models.Model):
    name = models.CharField(max_length=64, help_text='Name of Result')
    date = models.DateField(null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True,
                              limit_choices_to={'event_type': RACE})
    squad = models.ForeignKey(Squad, on_delete=models.SET_NULL, null=True, blank=True)
    distance = models.PositiveIntegerField(help_text='meters')
    minutes = models.PositiveIntegerField(default=0)
    seconds = models.DecimalField(max_digits=5, decimal_places=3, default=0,
                                  validators=[MinValueValidator(0), MaxValueValidator(59.999)])
    lightweight = models.BooleanField(default=False)
    rank = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), ])
    pace = models.FloatField(default=0)
    public = models.BooleanField(default=False)
    personal_record = models.BooleanField(default=False)

    shell = models.ForeignKey(
        Asset,
        on_delete=models.SET_NULL,
        limit_choices_to={'type': SHELL},
        null=True, blank=True,
    )
    coxswain = models.ForeignKey(
        Profile,
        on_delete=models.PROTECT,
        related_name='results_coxed',
        null=True, blank=True,
    )
    rowers = models.ManyToManyField(
        Profile,
        related_name='results_rowed',
        blank=True,
    )
    created_by = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        related_name='results_created',
        null=True, blank=True,
    )
    last_modified_by = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        related_name='results_last_modified',
        null=True, blank=True,
    )

    def __str__(self):
        return '%s (%s meters)' % (self.name, self.distance)

    def save(self, *args, **kwargs):
        user = CuserMiddleware.get_user()

        if user.is_staff:
            self.public = True
        else:
            self.public = False

        if not self.pk:
            self.created_by = user.profile
        self.last_modified_by = user.profile

        self.pace = self.get_pace()

        super(Result, self).save(*args, **kwargs)

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

    @property
    def absolute_url(self):
        return reverse_lazy('event:member_result_view', kwargs={'pk': self.pk})
