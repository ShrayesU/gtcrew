from cuser.middleware import CuserMiddleware
from django.db import models
# from django.urls import reverse_lazy
from django.db.models import Sum
from django.utils.text import slugify

from team.models import Profile


class Campaign(models.Model):
    title = models.CharField(unique=True, max_length=100)
    slug = models.SlugField(unique=True, max_length=100)
    goal = models.PositiveIntegerField()
    end_date = models.DateField()
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        Profile,
        on_delete=models.PROTECT,
        related_name='campaigns_created',
        null=True, blank=True,
    )
    last_modified_by = models.ForeignKey(
        Profile,
        on_delete=models.PROTECT,
        related_name='campaigns_last_modified',
        null=True, blank=True,
    )

    class Meta:
        ordering = ['-date_updated']

    def __str__(self):
        return '%s' % (self.title,)

    def save(self, *args, **kwargs):
        user = CuserMiddleware.get_user()
        if not self.pk:
            self.created_by = user.profile
        self.last_modified_by = user.profile
        if not self.slug:
            self.slug = slugify(self.title)
        super(Campaign, self).save(*args, **kwargs)

    @property
    def donation_total(self):
        if self.donation_set.exists():
            return self.donation_set.aggregate(sum=Sum('donation_amount'))['sum']
        else:
            return 0

    @property
    def goal_remaining(self):
        goal = int(self.goal)
        return max(0, goal-self.donation_total)

    # @property
    # def absolute_url(self):
    #     return reverse_lazy('story:view', kwargs={'slug': self.slug})


class Donation(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    donation_amount = models.PositiveIntegerField()

    donor = models.ForeignKey(
        Profile,
        on_delete=models.PROTECT,
        related_name='donations',
    )
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.PROTECT,
        null=True, blank=True,
    )
    created_by = models.ForeignKey(
        Profile,
        on_delete=models.PROTECT,
        related_name='donations_created',
        null=True, blank=True,
    )
    last_modified_by = models.ForeignKey(
        Profile,
        on_delete=models.PROTECT,
        related_name='donations_last_modified',
        null=True, blank=True,
    )

    def save(self, *args, **kwargs):
        user = CuserMiddleware.get_user()
        if not self.pk:
            self.created_by = user.profile
        self.last_modified_by = user.profile
        super(Donation, self).save(*args, **kwargs)
