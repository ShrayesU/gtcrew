from wagtail.admin.edit_handlers import StreamFieldPanel, FieldPanel
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock


class PostBlock(blocks.StructBlock):
    heading_small = blocks.CharBlock()
    heading_large = blocks.CharBlock()
    paragraph = blocks.RichTextBlock()
    photo = ImageChooserBlock()
    page = blocks.PageChooserBlock(required=False)
    document = DocumentChooserBlock(required=False)

    class Meta:
        icon = 'doc-empty'
        template = 'blocks/post_block.html'


class GenericPage(Page):
    body = StreamField([
        ('post', PostBlock())
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body')
    ]
