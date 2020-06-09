from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.snippets.blocks import SnippetChooserBlock

from team.models import Profile, Membership


class RosterPage(Page):
    # body = StreamField([
    #     ('profile', SnippetChooserBlock(Profile)),
    # ])
    #
    # content_panels = Page.content_panels + [
    #     StreamFieldPanel('body')
    # ]

    def get_context(self, request, *args, **kwargs):
        context = super(RosterPage, self).get_context(request)

        students = Membership.students.active()
        coaches = Membership.coaches.active()
        if students:
            officers = students.filter(title__held_by='student').order_by('title__sequence')
            context.update({'students': students,
                            'officers': officers, })
        if coaches:
            context.update({'coaches': coaches.order_by('title__sequence'), })

        return context
