from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.validators import RegexValidator
from django.db import models
from django.utils.text import slugify
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldRowPanel, FieldPanel, InlinePanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel

from event.models import BaseResult


class PersonalRecord(BaseResult):
    page = ParentalKey("person.PersonPage", related_name="personal_records")

    panels = BaseResult.result_panels


class PersonPage(Page):
    first_name = models.CharField(max_length=64, blank=False)
    last_name = models.CharField(max_length=64, blank=False)
    gtid = models.CharField("GT ID", max_length=9, blank=True,
                            validators=[RegexValidator(r'^(\d){9}$')])
    birthday = models.DateField(null=True, blank=True)
    major = models.CharField(max_length=64, blank=True)
    hometown = models.CharField(max_length=64, blank=True)
    bio = RichTextField(blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    class Meta:
        verbose_name_plural = 'People'

    @classmethod
    def autocomplete_create(cls: type, value: str):
        person_index_page = PersonIndexPage.objects.first()
        title = value
        split_value = value.split(' ')
        if len(split_value) == 1:
            first_name, last_name = value, value
        elif len(split_value) == 2:
            first_name, last_name = split_value
        else:
            first_name, last_name = split_value[0], ' '.join(split_value[1:])

        new = cls(title=title, first_name=first_name, last_name=last_name)
        person_index_page.add_child(instance=new)
        person_index_page.save()
        return new

    def clean(self):
        """Override the values of title and slug before saving."""
        super().clean()
        self.title = '%s %s' % (self.first_name, self.last_name)
        if not self.slug:
            self.slug = slugify(self.title)

    content_panels = [
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('first_name', classname="col6"),
                FieldPanel('last_name', classname="col6"),
            ])
        ], "Name"),
        ImageChooserPanel('image'),
        FieldPanel('bio', classname="collapsible"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('birthday', classname="col6"),
                FieldPanel('hometown', classname="col6"),
                FieldPanel('gtid', classname="col6"),
                FieldPanel('major', classname="col6"),
            ])
        ], "Details"),
        MultiFieldPanel(
            [InlinePanel("personal_records", label="Record")],
            heading="Personal Records", classname="collapsible"
        ),
    ]

    parent_page_types = ['PersonIndexPage']
    subpage_types = []


# # set a default blank slug for when the editing form renders
# # we set this after the model is declared
# PersonPage._meta.get_field('slug').default = 'default-blank-slug'


class PersonIndexPage(Page):
    max_count = 1
    subpage_types = ['PersonPage']

    def get_people(self):
        return PersonPage.objects.live().descendant_of(
            self).order_by('last_name')

    def paginate(self, request, *args):
        page = request.GET.get('page')
        paginator = Paginator(self.get_people(), 12)
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
        context = super(PersonIndexPage, self).get_context(request)

        # PersonPage objects (get_people) are passed through pagination
        people = self.get_people()  # self.paginate(request, self.get_people())

        context['people'] = people

        return context
