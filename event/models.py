from cuser.middleware import CuserMiddleware
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import pgettext_lazy

from asset.models import Asset
from asset.utils import SHELL
from event.utils import EVENT_TYPES, RACE
from team.models import Squad, Profile


class Event(models.Model):
    name = models.CharField(pgettext_lazy('Name of Event', 'Name'), max_length=64)
    location = models.CharField(pgettext_lazy('Location of Event', 'Location'), max_length=64)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(blank=True, null=True)
    event_type = models.CharField(pgettext_lazy('Type of Event', 'Type'), max_length=64, choices=EVENT_TYPES)
    squads = models.ManyToManyField(Squad)
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


class Result(models.Model):
    name = models.CharField(max_length=64, help_text='Name of Result')
    date = models.DateField(null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True,
                              limit_choices_to={'event_type': RACE})
    squad = models.ForeignKey(Squad, on_delete=models.SET_NULL, null=True, blank=True)
    time = models.CharField(pgettext_lazy('Official Time', 'Time'), blank=True, null=True,
                            max_length=9, help_text='MM:SS.mmm',
                            validators=[RegexValidator(r'^(\d){2}:(\d){2}.(\d){3}$')])
    distance = models.PositiveIntegerField(help_text='meters')
    minutes = models.PositiveIntegerField(default=0)
    seconds = models.DecimalField(max_digits=5, decimal_places=3, default=0,
                                  validators=[MinValueValidator(0), MaxValueValidator(59.999)])
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

        super(Result, self).save(*args, **kwargs)

    def total_time_string(self):
        """Returns string of total time"""
        return '{:02d}:{:06.3f}'.format(self.minutes, self.seconds)

    def pace(self):
        """Returns the pace rowed in the form of seconds per 500 meters."""
        seconds = float(self.minutes * 60) + float(self.seconds)
        five_hundred = float(self.distance) / 500
        return seconds / five_hundred

    def pace_string(self):
        """Returns pace in string format of MM:SS.mmm/Meters"""
        pace = self.pace()
        minutes, seconds = int(pace // 60), pace % 60
        return '{:02d}:{:06.3f}/500m'.format(minutes, seconds)

    def watts(self):
        """Returns the power in watts based on average pace per 500 meters."""
        pace = self.pace()
        return 2.80 / (pace ** 3)
