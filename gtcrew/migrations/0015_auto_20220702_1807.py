# Generated by Django 3.2.13 on 2022-07-02 22:07

from django.db import migrations
import wagtail.blocks
import wagtail.documents.blocks
import wagtail.embeds.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('gtcrew', '0014_auto_20220702_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formpage',
            name='body',
            field=wagtail.fields.StreamField([('post', wagtail.blocks.StructBlock([('heading_small', wagtail.blocks.CharBlock()), ('heading_large', wagtail.blocks.CharBlock()), ('paragraph', wagtail.blocks.RichTextBlock()), ('photo', wagtail.images.blocks.ImageChooserBlock()), ('page', wagtail.blocks.PageChooserBlock(required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(required=False))])), ('section', wagtail.blocks.StreamBlock([('heading_group_block', wagtail.blocks.StreamBlock([('heading', wagtail.blocks.StructBlock([('heading_text', wagtail.blocks.CharBlock(form_classname='title', required=True)), ('size', wagtail.blocks.ChoiceBlock(blank=True, choices=[('', 'Select a header size'), ('h2', 'H2'), ('h3', 'H3')]))]))])), ('paragraph_block', wagtail.blocks.RichTextBlock(icon='fa-paragraph', template='blocks/paragraph_block.html')), ('image_block', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('caption', wagtail.blocks.CharBlock(required=False)), ('attribution', wagtail.blocks.CharBlock(required=False))])), ('embed_block', wagtail.embeds.blocks.EmbedBlock(help_text='Insert an embed URL e.g https://www.youtube.com/embed/SGJFWirQ3ks', icon='fa-s15', template='blocks/embed_block.html'))]))], use_json_field=True),
        ),
        migrations.AlterField(
            model_name='genericpage',
            name='body',
            field=wagtail.fields.StreamField([('post', wagtail.blocks.StructBlock([('heading_small', wagtail.blocks.CharBlock()), ('heading_large', wagtail.blocks.CharBlock()), ('paragraph', wagtail.blocks.RichTextBlock()), ('photo', wagtail.images.blocks.ImageChooserBlock()), ('page', wagtail.blocks.PageChooserBlock(required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(required=False))])), ('section', wagtail.blocks.StreamBlock([('heading_group_block', wagtail.blocks.StreamBlock([('heading', wagtail.blocks.StructBlock([('heading_text', wagtail.blocks.CharBlock(form_classname='title', required=True)), ('size', wagtail.blocks.ChoiceBlock(blank=True, choices=[('', 'Select a header size'), ('h2', 'H2'), ('h3', 'H3')]))]))])), ('paragraph_block', wagtail.blocks.RichTextBlock(icon='fa-paragraph', template='blocks/paragraph_block.html')), ('image_block', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('caption', wagtail.blocks.CharBlock(required=False)), ('attribution', wagtail.blocks.CharBlock(required=False))])), ('embed_block', wagtail.embeds.blocks.EmbedBlock(help_text='Insert an embed URL e.g https://www.youtube.com/embed/SGJFWirQ3ks', icon='fa-s15', template='blocks/embed_block.html'))])), ('html', wagtail.blocks.RawHTMLBlock())], use_json_field=True),
        ),
    ]
