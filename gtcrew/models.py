from django.db import models
from django.forms import widgets
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel
from wagtail.contrib.forms.models import AbstractFormField, AbstractEmailForm
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail import blocks
from wagtail.fields import StreamField, RichTextField
from wagtail.models import Page
from wagtailcaptcha.models import WagtailCaptchaEmailForm

from gtcrew.blocks import PostBlock, BaseStreamBlock


class GenericPage(Page):
    body = StreamField([
        ('post', PostBlock()),
        ('section', BaseStreamBlock()),
        ('html', blocks.RawHTMLBlock()),
    ], use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('body')
    ]


class FormField(AbstractFormField):
    page = ParentalKey('FormPage', related_name='form_fields', on_delete=models.CASCADE)


class FormPage(WagtailCaptchaEmailForm):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    body = StreamField([
        ('post', PostBlock()),
        ('section', BaseStreamBlock())
    ], use_json_field=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('image'),
        FieldPanel('body'),
        InlinePanel('form_fields', label="Form fields", classname="form-control"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]

    subpage_types = []

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        for name, field in form.fields.items():
            if isinstance(field.widget, widgets.ChoiceWidget):
                css_classes = field.widget.attrs.get('class', '').split()
                css_classes.append('custom-select')
                field.widget.attrs.update({'class': ' '.join(css_classes)})
            else:
                css_classes = field.widget.attrs.get('class', '').split()
                css_classes.append('form-control')
                field.widget.attrs.update({'class': ' '.join(css_classes)})
            field.widget.attrs['aria-describedby'] = 'id_%s' % name  # slug version
            field.widget.attrs['aria-label'] = '%s' % field.label  # title version
            field.widget.attrs['placeholder'] = '%s' % field.label
        return form


@register_setting(icon='fa-picture-o')
class Favicon(BaseSiteSetting):
    favicon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel('favicon'),
    ]


@register_setting(icon='fa-id-card-o')
class Registration(BaseSiteSetting):
    open_registration = models.BooleanField(default=True)

    panels = [
        FieldPanel('open_registration'),
    ]
