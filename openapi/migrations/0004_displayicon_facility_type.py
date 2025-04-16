# Generated by Django 5.2 on 2025-04-16 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openapi', '0003_displayicon_alter_safetyfacility_facility_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='displayicon',
            name='facility_type',
            field=models.CharField(choices=[('001', '경찰서'), ('002', 'CCTV'), ('003', '안전시설물'), ('004', '안전지킴이집')], default=1, max_length=10),
            preserve_default=False,
        ),
    ]
