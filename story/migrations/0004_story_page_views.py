# Generated by Django 3.0.4 on 2020-04-18 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0003_auto_20200415_2132'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='page_views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
