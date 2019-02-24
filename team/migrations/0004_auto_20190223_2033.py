# Generated by Django 2.0.7 on 2019-02-24 01:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0003_auto_20190223_1511'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emailaddress',
            options={'verbose_name_plural': 'email addresses'},
        ),
        migrations.AddField(
            model_name='emailaddress',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
