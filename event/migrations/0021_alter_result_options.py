# Generated by Django 4.1.13 on 2024-04-24 15:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0020_alter_eventpage_event_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='result',
            options={'ordering': ['-date', 'pace']},
        ),
    ]
