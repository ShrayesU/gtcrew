from cuser.middleware import CuserMiddleware
from django.db import models
from django.urls import reverse_lazy

from asset.utils import ASSET_TYPE_CHOICES, SHELL
from team.models import Profile


class Asset(models.Model):
    name = models.CharField(unique=True, max_length=100)
    serial_number = models.CharField(null=True, blank=True, max_length=100)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(
        max_length=6,
        choices=ASSET_TYPE_CHOICES,
        default=SHELL,
    )
    acquisition_date = models.DateField(null=True, blank=True, help_text='Date of purchase.')
    acquisition_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    retirement_date = models.DateField(null=True, blank=True, help_text='Date removed from service.')
    retirement_reason = models.TextField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        Profile,
        on_delete=models.PROTECT,
        related_name='assets_created',
    )
    last_modified_by = models.ForeignKey(
        Profile,
        on_delete=models.PROTECT,
        related_name='assets_last_modified',
    )

    class Meta:
        ordering = ['-date_updated']

    def __str__(self):
        return '%s' % (self.name,)

    def save(self, *args, **kwargs):
        user = CuserMiddleware.get_user()
        if not self.pk:
            self.created_by = user.profile
        self.last_modified_by = user.profile
        super(Asset, self).save(*args, **kwargs)

    @property
    def absolute_url(self):
        return reverse_lazy('asset:view', kwargs={'pk': self.pk})
