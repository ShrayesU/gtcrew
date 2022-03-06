from django.db import models
from django.utils.translation import pgettext_lazy
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, FieldRowPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class ShellSize(models.Model):
    size = models.CharField(max_length=10)

    def __str__(self):
        return self.size

    @classmethod
    def autocomplete_create(cls: type, value: str):
        return cls.objects.create(size=value)


class ShellPage(Page):
    manufacturer = models.CharField(pgettext_lazy('Manufacturer', 'Manufacturer'), max_length=64)
    size = models.ForeignKey(
        'shell.ShellSize',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    date_acquired = models.DateField(blank=True, null=True)
    date_decommissioned = models.DateField(blank=True, null=True)
    # decommissioned = models.BooleanField(default=False)
    description = RichTextField(blank=True, null=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('manufacturer'),
        SnippetChooserPanel('size'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('date_acquired', classname='col6'),
                FieldPanel('date_decommissioned', classname='col6'),
            ])
        ], heading='Dates'),
        FieldPanel('description'),
        ImageChooserPanel('image'),
    ]

    parent_page_types = ['ShellIndexPage']
    subpage_types = []

    # def save(self, *args, **kwargs):
    #     self.decommissioned = bool(self.date_decommissioned)
    #     super().save(*args, **kwargs)


class ShellIndexPage(Page):
    subpage_types = ['ShellPage']
    max_count = 1

    def get_shells(self):
        return ShellPage.objects.live().descendant_of(self).order_by('-date_acquired', '-date_decommissioned')

    def get_context(self, request, *args, **kwargs):
        context = super(ShellIndexPage, self).get_context(request)

        shells = self.get_shells()
        context['shells'] = shells

        return context
