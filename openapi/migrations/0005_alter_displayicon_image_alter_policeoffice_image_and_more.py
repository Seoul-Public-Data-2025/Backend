# Generated by Django 5.2 on 2025-04-18 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openapi', '0004_displayicon_phonenumber_policeoffice_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='displayicon',
            name='image',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='policeoffice',
            name='image',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='safetyfacility',
            name='image',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='safetyservice',
            name='image',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
