from django.db import models
#from django.contrib.auth import get_user_model
from django.utils.timezone import now
#from django.db.models.signals import post_save
#from django.dispatch import receiver
from django.core.validators import RegexValidator

#User = get_user_model()
# default to current year
def get_default_year():
  return now().year

class Profile(models.Model):
    first_name = models.CharField(max_length=64, blank=False)
    last_name = models.CharField(max_length=64, blank=False)
    email = models.EmailField(unique=True)
    gtid = models.CharField("GT ID", blank=True, max_length=9,
        validators=[RegexValidator(r'^\d{1,10}$')])
    birthday = models.DateField(null=True, blank=True)
    major = models.CharField(max_length=64, blank=True)
    hometown = models.CharField(max_length=64, blank=True)
    bio = models.TextField(max_length=1500, blank=True)
    date_created = models.DateTimeField('date created', auto_now_add=True)
    date_updated = models.DateTimeField('date updated', auto_now=True)
    photo = models.FileField(null=True, blank=True)

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'
        ordering = ['-date_updated']

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def latest_year_active(self):
        return Membership.objects.filter(profile=self.id).latest('year').year
"""
    def save(self, *args, **kwargs):
        if not self.id:
            self.date_created = now()
        self.date_updated = now()
        super(Profile, self).save(*args, **kwargs)
"""
"""
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
"""
class Title(models.Model):
    title = models.CharField(max_length=64)
    sequence = models.PositiveSmallIntegerField(default=0)
    STUDENT = 'student'
    COACH = 'coach'
    ALUMNI = 'alumni'
    HELD_BY_CHOICES = (
        (STUDENT, 'Student'),
        (COACH, 'Coach'),
        (ALUMNI, 'Alumni'),
    )
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
        return '%s' % (self.squad)

class Award(models.Model):
    award = models.CharField(max_length=64, unique=True)
    description = models.TextField()
    profiles = models.ManyToManyField(
        Profile,
        through='AwardGiven',
        through_fields=('award', 'profile')
    )

    def __str__(self):
        return '%s' % (self.award)

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
    FALL = 'FALL'
    SPRING = 'SPRING'
    SEMESTER_CHOICES = (
        (FALL, 'Fall'),
        (SPRING, 'Spring'),
    )
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

    def __str__(self):
        return '%s%s: %s' % (self.semester, self.year, self.profile)

    def season(self):
        TEAM_FOUNDED = 1985
        if self.semester == self.FALL:
            return self.year - (TEAM_FOUNDED-1)
        else:
            return self.year - TEAM_FOUNDED

class TextGroup(models.Model):
    text = models.TextField(max_length=500, blank=True)
    header1 = models.CharField('small header', max_length=64, blank=True)
    header2 = models.CharField('large header', max_length=64, blank=True)

    class Meta:
        abstract = True

class Page(TextGroup):
    page = models.CharField(max_length=64, unique=True)
    sequence = models.PositiveIntegerField(unique=True)
    test = models.TextField(max_length=500, blank=True)
    DEFAULT = 'BASE'
    HOME = 'HOME'
    ABOUT = 'ABOUT'
    TEAM = 'TEAM'
    TEMPLATE_CHOICES = (
        (DEFAULT, 'Regular'),
        (HOME, 'Home'),
        (ABOUT, 'About'),
        (TEAM, 'Team'),
    )
    template = models.CharField(
        max_length=5,
        choices=TEMPLATE_CHOICES,
        default=DEFAULT,
    )

    def __str__(self):
        return '%s' % (self.page)

class Post(TextGroup):
    photo = models.FileField()
    additional_link = models.URLField(blank=True)
    additional_link_text = models.CharField(max_length=30, blank=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s' % (self.header1, self.header2)
