from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import InlinePanel, PageChooserPanel, MultiFieldPanel, FieldRowPanel, FieldPanel
from wagtail.core.models import Page, Orderable
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtailautocomplete.edit_handlers import AutocompletePanel

from person.models import PersonPage
from team.utils import COACH, STUDENT


class Coach(Orderable):
    page = ParentalKey("roster.TermPage", related_name="coaches")
    person_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='+',
    )
    position = models.ForeignKey(
        'team.Title',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='+',
        limit_choices_to={'held_by': COACH},
    )
    squad = models.ForeignKey(
        'team.Squad',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='+',
    )

    class Meta:
        verbose_name_plural = 'Coaches'

    def __str__(self):
        return '%s %s' % (self.person_page.specific.first_name, self.person_page.specific.last_name)

    panels = [
        PageChooserPanel('person_page', 'person.PersonPage'),
        SnippetChooserPanel('position'),
        SnippetChooserPanel('squad'),
    ]


class Officers(Orderable):
    page = ParentalKey("roster.TermPage", related_name="officers")
    person_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='+',
        help_text='You can only search for a Published person page. '
                  '"Create New" only works if you have Publish permissions.'
        # limit_choices_to={'live': True},
    )
    position = models.ForeignKey(
        'team.Title',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='+',
        limit_choices_to={'held_by': STUDENT},
    )

    def __str__(self):
        return '%s %s' % (self.person_page.specific.first_name, self.person_page.specific.last_name)

    panels = [
        AutocompletePanel('person_page', 'person.PersonPage'),
        SnippetChooserPanel('position'),
    ]


class Member(models.Model):
    page = ParentalKey("roster.TermPage", related_name="members")
    person_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='+',
        help_text='You can only search for a Published person page. '
                  '"Create New" only works if you have Publish permissions.'
    )

    def __str__(self):
        return '%s %s' % (self.person_page.specific.first_name, self.person_page.specific.last_name)

    panels = [AutocompletePanel('person_page', 'person.PersonPage')]


class TermPage(Page):
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('start_date', classname="col6"),
                FieldPanel('end_date', classname="col6"),
            ])
        ], heading="Term"),
        MultiFieldPanel(
            [InlinePanel("coaches", label="Person")],
            heading="Coaches", classname="collapsible"
        ),
        MultiFieldPanel(
            [InlinePanel("officers", label="Person")],
            heading="Officers", classname="collapsible"
        ),
        MultiFieldPanel(
            [InlinePanel("members", label="Person")],
            heading="Members", classname="collapsible"
        ),
    ]

    parent_page_types = ['roster.RosterIndexPage']
    subpage_types = []

    def get_context(self, request, *args, **kwargs):
        context = super(TermPage, self).get_context(request)

        members = PersonPage.objects.live().filter(
            id__in=self.members.all().values('person_page_id')
        ).order_by('last_name')
        context['members'] = members

        return context


class RosterIndexPage(Page):
    subpage_types = ['TermPage']

    def get_terms(self):
        return TermPage.objects.live().descendant_of(
            self).order_by('-start_date')

    def paginate(self, request, *args):
        page = request.GET.get('page')
        paginator = Paginator(self.get_terms(), 12)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        return pages

    # Returns the above to the get_context method that is used to populate the
    # template
    def get_context(self, request, *args, **kwargs):
        context = super(RosterIndexPage, self).get_context(request)

        # PersonPage objects (get_people) are passed through pagination
        terms = self.paginate(request, self.get_terms())

        context['terms'] = terms

        return context
