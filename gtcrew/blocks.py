from wagtail.core import blocks
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
