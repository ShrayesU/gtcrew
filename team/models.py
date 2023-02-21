from cuser.middleware import CuserMiddleware
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse_lazy
from django.utils.timezone import now
from django_resized import ResizedImageField
from modelcluster.fields import ParentalManyToManyField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, FieldRowPanel
from wagtail.fields import RichTextField
from wagtail.models import WorkflowMixin, DraftStateMixin, LockableMixin, RevisionMixin
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from .managers import StudentManager, CoachManager
from .utils import HELD_BY_CHOICES, STUDENT, SEMESTER_CHOICES, FALL, TEAM_FOUNDED, \
    PROFILE_STATUS_CHOICES, UNCLAIMED


def get_default_year():
    return now().year


@register_snippet
class Profile(WorkflowMixin, DraftStateMixin, RevisionMixin, LockableMixin, index.Indexed, models.Model):
    first_name = models.CharField(max_length=64, blank=False)
    last_name = models.CharField(max_length=64, blank=False)
    gtid = models.CharField("GT ID", max_length=9, blank=True,
                            validators=[RegexValidator(r'^(\d){9}$')])
    birthday = models.DateField(null=True, blank=True)
    major = models.CharField(max_length=64, blank=True)
    hometown = models.CharField(max_length=64, blank=True)
    bio = RichTextField(max_length=1500, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    public = models.BooleanField(default=False)
    photo = ResizedImageField(size=[700, 700], crop=['middle', 'center'], null=True, blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    status = models.CharField(
        max_length=10,
        choices=PROFILE_STATUS_CHOICES,
        default=UNCLAIMED,
    )
    owner = models.OneToOneField(
        get_user_model(),
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    _revisions = GenericRelation("wagtailcore.Revision", related_query_name='profile')

    class Meta:
        ordering = ['last_name']

    panels = [
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('first_name', classname="col6"),
                FieldPanel('last_name', classname="col6"),
            ])
        ], "Name"),
        FieldPanel('image'),
        MultiFieldPanel([
            FieldPanel('owner'),
            FieldPanel('status'),
            FieldPanel('public'),
        ], "Administrative",
            classname="collapsible collapsed"
        ),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('birthday', classname="col6"),
                FieldPanel('hometown', classname="col6"),
                FieldPanel('gtid', classname="col6"),
                FieldPanel('major', classname="col6"),
            ])
        ], "Details"),
        FieldPanel('bio'),
    ]
    search_fields = [
        index.SearchField('first_name', partial_match=True),
        index.SearchField('last_name', partial_match=True),
        index.SearchField('gtid', partial_match=True),
        index.FilterField('status'),
    ]

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        user = CuserMiddleware.get_user()
        if user.is_staff:
            self.public = True
        super(Profile, self).save(*args, **kwargs)

    @property
    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    @property
    def latest_year_active(self):
        return self.membership_set.latest('year').year

    @property
    def latest_email(self):
        return self.emailaddress_set.latest().email

    @property
    def absolute_url(self):
        return reverse_lazy('team:view_profile', kwargs={'pk': self.pk})

    @property
    def revisions(self):
        return self._revisions


class EmailAddress(models.Model):
    email = models.EmailField(unique=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'email addresses'
        ordering = ['-date_added']
        get_latest_by = ['date_added']

    def __str__(self):
        return '%s' % self.email


@register_snippet
class Title(WorkflowMixin, DraftStateMixin, RevisionMixin, index.Indexed, models.Model):
    title = models.CharField(max_length=64)
    sequence = models.PositiveSmallIntegerField(default=0)
    held_by = models.CharField(
        max_length=7,
        choices=HELD_BY_CHOICES,
        default=STUDENT,
    )
    profiles = ParentalManyToManyField(
        Profile,
        through='Membership',
        through_fields=('title', 'profile'),
        blank=True,
    )
    _revisions = GenericRelation("wagtailcore.Revision", related_query_name='title')

    def __str__(self):
        return '%s: %s' % (self.held_by, self.title)

    panels = [
        FieldPanel('title'),
        FieldPanel('held_by'),
        FieldPanel('sequence'),
    ]

    search_fields = [
        index.SearchField('title', partial_match=True),
        index.FilterField('held_by'),
    ]

    @property
    def revisions(self):
        return self._revisions


@register_snippet
class Squad(models.Model):
    squad = models.CharField(max_length=64)
    profiles = models.ManyToManyField(
        Profile,
        through='Membership',
        through_fields=('squad', 'profile',),
        blank=True,
    )

    def __str__(self):
        return '%s' % self.squad

    panels = [
        FieldPanel('squad'),
    ]


@register_snippet
class Membership(models.Model):
    semester = models.CharField(
        max_length=6,
        choices=SEMESTER_CHOICES,
        default=FALL,
    )
    year = models.PositiveIntegerField(default=get_default_year)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    squad = models.ForeignKey(
        Squad,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    public = models.BooleanField(default=False)

    objects = models.Manager()
    students = StudentManager()
    coaches = CoachManager()

    class Meta:
        ordering = ['year', '-semester']

    panels = [
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('semester', classname="col6"),
                FieldPanel('year', classname="col6"),
            ])
        ], "Semester"),
        FieldPanel('profile'),
        FieldPanel('squad'),
        FieldPanel('title'),
        FieldPanel('public'),
    ]
    search_fields = [
        index.SearchField('profile__first_name', partial_match=True),
        index.SearchField('profile__last_name', partial_match=True),
        index.SearchField('profile__gtid', partial_match=True),
        index.FilterField('title'),
    ]

    def __str__(self):
        return '%s%s: %s' % (self.semester, self.year, self.profile)

    def save(self, *args, **kwargs):
        user = CuserMiddleware.get_user()
        if user.is_staff:
            self.public = True
        super(Membership, self).save(*args, **kwargs)

    def season(self):
        if self.semester == FALL:
            return self.year - (TEAM_FOUNDED - 1)
        else:
            return self.year - TEAM_FOUNDED
