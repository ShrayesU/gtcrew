from cuser.middleware import CuserMiddleware
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

from team.models import Profile


class Story(models.Model):
    title = models.CharField(unique=True, max_length=100)
    story = models.TextField()
    slug = models.SlugField(unique=True, max_length=100)
    page_views = models.PositiveIntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    profiles_mentioned = models.ManyToManyField(
        Profile,
        blank=True,
        related_name='stories_mentioned',
    )

    created_by = models.ForeignKey(
        Profile,
        on_delete=models.PROTECT,
        related_name='stories_created',
    )

    class Meta:
        verbose_name = 'story'
        verbose_name_plural = 'stories'
        ordering = ['-date_updated']

    def __str__(self):
        return '%s' % (self.title,)

    def save(self, *args, **kwargs):
        user = CuserMiddleware.get_user()
        if not self.pk:
            self.created_by = user.profile
        if not self.slug:
            self.slug = slugify(self.title)
        super(Story, self).save(*args, **kwargs)
