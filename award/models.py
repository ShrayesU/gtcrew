from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page
from django.db import models
from wagtail.snippets.models import register_snippet
from wagtailautocomplete.edit_handlers import AutocompletePanel

from common.utils import get_current_year


@register_snippet
class Recipient(models.Model):
    page = ParentalKey("award.AwardPage", related_name="recipients")
    person_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='+',
    )
    year = models.PositiveIntegerField(default=get_current_year)

    panels = [
        AutocompletePanel('page', 'award.AwardPage'),
        AutocompletePanel('person_page', 'person.PersonPage'),
        FieldPanel('year'),
    ]

    def __str__(self):
        return '%s of %s' % (self.page, self.year)


class AwardPage(Page):
    description = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        MultiFieldPanel(
            [InlinePanel("recipients", label="Recipient")],
            heading="Recipients", classname="collapsible"
        ),
    ]

    parent_page_types = ['AwardIndexPage']
    subpage_types = ['gtcrew.GenericPage']

    def get_recipients(self):
        return self.recipients.all().order_by('-year')

    def get_context(self, request, *args, **kwargs):
        context = super(AwardPage, self).get_context(request)

        recipients = self.get_recipients()
        context['recipients'] = recipients

        return context


class AwardIndexPage(Page):
    subpage_types = ['AwardPage', 'gtcrew.GenericPage']
    max_count = 1

    def get_awards(self):
        return AwardPage.objects.live().descendant_of(self)

    def get_context(self, request, *args, **kwargs):
        context = super(AwardIndexPage, self).get_context(request)

        awards = self.get_awards()
        context['awards'] = awards

        return context
