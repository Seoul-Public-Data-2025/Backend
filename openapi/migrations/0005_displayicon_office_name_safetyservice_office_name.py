# Generated by Django 5.2 on 2025-04-16 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openapi', '0004_displayicon_facility_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='displayicon',
            name='office_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='OfficeName'),
        ),
        migrations.AddField(
            model_name='safetyservice',
            name='office_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='OfficeName'),
        ),
    ]
