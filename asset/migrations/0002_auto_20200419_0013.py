# Generated by Django 3.0.4 on 2020-04-19 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='acquisition_date',
            field=models.DateField(blank=True, help_text='Date of purchase.', null=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='acquisition_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='retirement_date',
            field=models.DateField(blank=True, help_text='Date removed from service.', null=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='retirement_reason',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='serial_number',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
