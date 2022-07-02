# Generated by Django 3.0.4 on 2020-06-11 16:14

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0045_assign_unlock_grouppagepermission'),
        ('team', '0016_profile_image'),
        ('event', '0009_auto_20200523_1400'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='Regatta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ResultPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('date', models.DateField(blank=True, null=True)),
                ('entry', models.CharField(help_text='E.g. "Lightweight Varsity 8+"', max_length=64)),
                ('distance', models.PositiveIntegerField(help_text='meters')),
                ('minutes', models.PositiveIntegerField(default=0)),
                ('seconds', models.DecimalField(decimal_places=3, default=0, max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(59.999)])),
                ('lightweight', models.BooleanField(default=False)),
                ('rank', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('pace', models.FloatField(default=0, editable=False)),
                ('squad', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='team.Squad')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='EventPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('location', models.CharField(max_length=64, verbose_name='Location')),
                ('start_datetime', models.DateTimeField()),
                ('end_datetime', models.DateTimeField(blank=True, null=True)),
                ('event_type', models.CharField(choices=[('Race', 'Race'), ('Administrative', 'Administrative'), ('Social', 'Social')], default='Race', max_length=64, verbose_name='Type')),
                ('description', wagtail.fields.RichTextField(blank=True, null=True)),
                ('regatta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='event.Regatta')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
