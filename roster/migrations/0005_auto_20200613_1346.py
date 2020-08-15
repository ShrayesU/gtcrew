# Generated by Django 3.0.7 on 2020-06-13 17:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0045_assign_unlock_grouppagepermission'),
        ('roster', '0004_auto_20200613_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='person_page',
            field=models.ForeignKey(blank=True, help_text='You can only search for a Published person page. "Create New" only works if you have Publish permissions.', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='wagtailcore.Page'),
        ),
        migrations.AlterField(
            model_name='officers',
            name='person_page',
            field=models.ForeignKey(blank=True, help_text='You can only search for a Published person page. "Create New" only works if you have Publish permissions.', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='wagtailcore.Page'),
        ),
    ]