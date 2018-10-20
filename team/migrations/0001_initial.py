# Generated by Django 2.0.7 on 2018-10-20 22:12

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import team.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('award', models.CharField(max_length=64, unique=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='AwardGiven',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveIntegerField(default=team.models.get_default_year)),
                ('award', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='team.Award')),
            ],
            options={
                'ordering': ['-year'],
                'verbose_name_plural': 'awards given',
                'verbose_name': 'award given',
            },
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.CharField(choices=[('FALL', 'Fall'), ('SPRING', 'Spring')], default='FALL', max_length=6)),
                ('year', models.PositiveIntegerField(default=team.models.get_default_year)),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, max_length=500)),
                ('header1', models.CharField(blank=True, max_length=64, verbose_name='small header')),
                ('header2', models.CharField(blank=True, max_length=64, verbose_name='large header')),
                ('page', models.CharField(max_length=64, unique=True)),
                ('sequence', models.PositiveIntegerField(unique=True)),
                ('test', models.TextField(blank=True, max_length=500)),
                ('template', models.CharField(choices=[('BASE', 'Regular'), ('HOME', 'Home'), ('ABOUT', 'About'), ('TEAM', 'Team')], default='BASE', max_length=5)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, max_length=500)),
                ('header1', models.CharField(blank=True, max_length=64, verbose_name='small header')),
                ('header2', models.CharField(blank=True, max_length=64, verbose_name='large header')),
                ('photo', models.FileField(upload_to='')),
                ('additional_link', models.URLField(blank=True)),
                ('additional_link_text', models.CharField(blank=True, max_length=30)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('page', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='team.Page')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('gtid', models.CharField(blank=True, max_length=9, validators=[django.core.validators.RegexValidator('^\\d{1,10}$')], verbose_name='GT ID')),
                ('birthday', models.DateField(blank=True, null=True)),
                ('major', models.CharField(blank=True, max_length=64)),
                ('hometown', models.CharField(blank=True, max_length=64)),
                ('bio', models.TextField(blank=True, max_length=1500)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='date updated')),
                ('photo', models.FileField(blank=True, null=True, upload_to='')),
            ],
            options={
                'ordering': ['-date_updated'],
                'verbose_name_plural': 'profiles',
                'verbose_name': 'profile',
            },
        ),
        migrations.CreateModel(
            name='Squad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('squad', models.CharField(max_length=64)),
                ('profiles', models.ManyToManyField(through='team.Membership', to='team.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('sequence', models.PositiveSmallIntegerField(default=0)),
                ('held_by', models.CharField(choices=[('student', 'Student'), ('coach', 'Coach'), ('alumni', 'Alumni')], default='student', max_length=7)),
                ('profiles', models.ManyToManyField(through='team.Membership', to='team.Profile')),
            ],
        ),
        migrations.AddField(
            model_name='membership',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='team.Profile'),
        ),
        migrations.AddField(
            model_name='membership',
            name='squad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='team.Squad'),
        ),
        migrations.AddField(
            model_name='membership',
            name='title',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='team.Title'),
        ),
        migrations.AddField(
            model_name='awardgiven',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='team.Profile'),
        ),
        migrations.AddField(
            model_name='award',
            name='profiles',
            field=models.ManyToManyField(through='team.AwardGiven', to='team.Profile'),
        ),
    ]
