# Generated by Django 3.2.5 on 2021-07-24 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0002_auto_20200419_0013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]