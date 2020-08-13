from cuser.middleware import CuserMiddleware
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models
# from django.urls import reverse_lazy
from django.db.models import Sum
from django.utils.text import slugify
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import StreamFieldPanel, PageChooserPanel, FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.core.blocks import PageChooserBlock
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core.models import Page
from wagtailautocomplete.edit_handlers import AutocompletePanel

from gtcrew.blocks import PostBlock, BaseStreamBlock
from team.models import Profile


class Donor(models.Model):
    page = ParentalKey("campaign.CampaignPage", related_name="donors")
    person_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='+',
        help_text='You can only search for a Published person page. '
                  '"Create New" only works if you have Publish permissions.'
    )
    amount = models.DecimalField(max_digits=9, decimal_places=2,
                                 help_text="Internal use only. Amount remains hidden from the public.")
    date_donated = models.DateField()
    anonymous = models.BooleanField(default=False,
                                    help_text='"George P. Burdell" will replace name of donor on campaign page.')

    def __str__(self):
        return '%s %s' % (self.person_page.specific.first_name, self.person_page.specific.last_name)

    panels = [
        AutocompletePanel('person_page', 'person.PersonPage'),
        FieldPanel('amount'),
        FieldPanel('date_donated'),
        FieldPanel('anonymous'),
    ]


class CampaignPage(Page):
    goal = models.PositiveIntegerField()
    end_date = models.DateField()
    description = RichTextField()
    interest_form = models.ForeignKey(
        'gtcrew.FormPage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Provide a FormPage for users to submit interest in donating."
    )

    content_panels = Page.content_panels + [
        FieldPanel('goal'),
        FieldPanel('end_date'),
        FieldPanel('description'),
        PageChooserPanel('interest_form'),
        MultiFieldPanel(
            [InlinePanel("donors", label="Person")],
            heading="Donors", classname="collapsible"
        ),
    ]

    parent_page_types = ['campaign.DonateIndexPage']
    subpage_types = ['gtcrew.FormPage']

    @property
    def donation_total(self):
        if self.donors.exists():
            return sum(donor.amount for donor in self.donors.all())
        else:
            return 0

    @property
    def goal_remaining(self):
        goal = int(self.goal)
        return max(0, goal - self.donation_total)

    def get_donors(self):
        if self.donors.exists():
            return sorted(self.donors.all(), key=str)
        else:
            return None

    def get_context(self, request, *args, **kwargs):
        context = super(CampaignPage, self).get_context(request)

        donors = self.get_donors()
        context['donors'] = donors

        return context


class DonateIndexPage(Page):
    body = StreamField([
        ('post', PostBlock()),
        ('section', BaseStreamBlock()),
    ])
    featured_section = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Featured section for the donation page. Will display the beginning '
                  'of the campaign description, as well as an infographic.',
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
        PageChooserPanel('featured_section', 'campaign.CampaignPage')
    ]

    subpage_types = ['campaign.CampaignPage']

    def get_campaigns(self):
        return CampaignPage.objects.live().descendant_of(
            self).order_by('-end_date')

    def paginate(self, request, *args):
        page = request.GET.get('page')
        paginator = Paginator(self.get_campaigns(), 12)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        return pages

    def get_context(self, request, *args, **kwargs):
        context = super(DonateIndexPage, self).get_context(request)

        campaigns = self.paginate(request, self.get_campaigns())

        context['campaigns'] = campaigns

        return context


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
        return max(0, goal - self.donation_total)

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
