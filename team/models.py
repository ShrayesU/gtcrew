from django_resized import ResizedImageField
from django.core.validators import RegexValidator
from django.db import models
from django.utils.timezone import now
from django.contrib.auth import get_user_model

from .managers import StudentManager, CoachManager
from .utils import HELD_BY_CHOICES, STUDENT, SEMESTER_CHOICES, FALL, TEMPLATE_CHOICES, DEFAULT, TEAM_FOUNDED
from .validators import validate_file_extension


def get_default_year():
    return now().year


class Profile(models.Model):
    first_name = models.CharField(max_length=64, blank=False)
    last_name = models.CharField(max_length=64, blank=False)
    gtid = models.CharField("GT ID", unique=True, max_length=9,
                            validators=[RegexValidator(r'^(\d){9}$')])
    birthday = models.DateField(null=True, blank=True)
    major = models.CharField(max_length=64, blank=True)
    hometown = models.CharField(max_length=64, blank=True)
    bio = models.TextField(max_length=1500, blank=True)
    date_created = models.DateTimeField('date created', auto_now_add=True)
    date_updated = models.DateTimeField('date updated', auto_now=True)
    photo = ResizedImageField(size=[700, 700], crop=['middle', 'center'], null=True, blank=True)
    owner = models.OneToOneField(
        get_user_model(),
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'
        ordering = ['-date_updated']

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def latest_year_active(self):
        return self.membership_set.latest('year').year

    def latest_email(self):
        return self.emailaddress_set.latest().email


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


class Title(models.Model):
    title = models.CharField(max_length=64)
    sequence = models.PositiveSmallIntegerField(default=0)
    held_by = models.CharField(
        max_length=7,
        choices=HELD_BY_CHOICES,
        default=STUDENT,
    )
    profiles = models.ManyToManyField(
        Profile,
        through='Membership',
        through_fields=('title', 'profile')
    )

    def __str__(self):
        return '%s: %s' % (self.held_by, self.title)


class Squad(models.Model):
    squad = models.CharField(max_length=64)
    profiles = models.ManyToManyField(
        Profile,
        through='Membership',
        through_fields=('squad', 'profile',)
    )

    def __str__(self):
        return '%s' % self.squad


class Award(models.Model):
    award = models.CharField(max_length=64, unique=True)
    description = models.TextField()
    profiles = models.ManyToManyField(
        Profile,
        through='AwardGiven',
        through_fields=('award', 'profile')
    )

    def __str__(self):
        return '%s' % self.award


class AwardGiven(models.Model):
    award = models.ForeignKey(Award, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    year = models.PositiveIntegerField(default=get_default_year)

    class Meta:
        verbose_name = 'award given'
        verbose_name_plural = 'awards given'
        ordering = ['-year']

    def __str__(self):
        return '%s - %s' % (self.year, self.award)


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
    objects = models.Manager()
    students = StudentManager()
    coaches = CoachManager()

    def __str__(self):
        return '%s%s: %s' % (self.semester, self.year, self.profile)

    def season(self):
        if self.semester == FALL:
            return self.year - (TEAM_FOUNDED - 1)
        else:
            return self.year - TEAM_FOUNDED


class TextGroup(models.Model):
    text = models.TextField(max_length=500, blank=True)
    header1 = models.CharField('small header', max_length=64, blank=True)
    header2 = models.CharField('large header', max_length=64, blank=True)

    class Meta:
        abstract = True


class Page(models.Model):
    page = models.CharField(max_length=64, unique=True)
    sequence = models.PositiveIntegerField(unique=True)
    template = models.CharField(
        max_length=5,
        choices=TEMPLATE_CHOICES,
        default=DEFAULT,
    )

    def __str__(self):
        return '%s' % self.page


class Post(TextGroup):
    photo = models.ImageField(blank=True, null=True)
    additional_link = models.URLField(blank=True)
    additional_link_text = models.CharField(max_length=30, blank=True)
    document = models.FileField(blank=True, validators=[validate_file_extension])
    document_name = models.CharField(max_length=30, blank=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s' % (self.header1, self.header2)
