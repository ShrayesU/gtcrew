from cuser.middleware import CuserMiddleware
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

from team.models import Profile


class Story(models.Model):
    title = models.CharField(max_length=100)
    story = models.TextField()
    slug = models.SlugField(unique=True, max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    profiles_mentioned = models.ManyToManyField(
        Profile,
        blank=True,
    )

    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'
        ordering = ['-date_updated']

    def __str__(self):
        return '%s' % (self.title,)

    def save(self, *args, **kwargs):
        user = CuserMiddleware.get_user()
        if not self.pk:
            self.created_by = user
        if not self.slug:
            self.slug = slugify(self.title)
        super(Story, self).save(*args, **kwargs)
