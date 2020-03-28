from django.core.validators import RegexValidator, MinValueValidator
from django.db import models
from django.utils.translation import pgettext_lazy

from event.utils import EVENT_TYPES
from team.models import Squad


class Event(models.Model):
    name = models.CharField(pgettext_lazy('Name of Event', 'Name'), max_length=64)
    location = models.CharField(pgettext_lazy('Location of Event', 'Location'), max_length=64)
    start_datetime = models.DateTimeField(blank=False, null=False)
    end_datetime = models.DateTimeField(blank=True, null=True)
    event_type = models.CharField(pgettext_lazy('Type of Event', 'Type'), max_length=64, choices=EVENT_TYPES)
    squads = models.ManyToManyField(Squad)
    description = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_datetime']

    def __str__(self):
        return '%s %s' % (self.name, self.start_datetime.year)


class Result(models.Model):
    name = models.CharField(pgettext_lazy('Name of Racing Event', 'Name'), max_length=64)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=False, blank=False,
                              limit_choices_to={'event_type': 'Race'})
    squad = models.ForeignKey(Squad, on_delete=models.CASCADE, null=True, blank=True)
    time = models.CharField(pgettext_lazy('Official Time', 'Time'), blank=True, null=True,
                            max_length=9, help_text='MM:SS.mmm',
                            validators=[RegexValidator(r'^(\d){2}:(\d){2}.(\d){3}$')])
    distance = models.IntegerField(blank=True, null=True, help_text='meters',
                                   validators=[MinValueValidator(0)])

    def __str__(self):
        return '%s (%s)' % (self.name, self.event)
