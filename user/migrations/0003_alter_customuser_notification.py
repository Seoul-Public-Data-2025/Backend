# Generated by Django 5.2 on 2025-04-16 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_customuser_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='notification',
            field=models.BooleanField(default=True),
        ),
    ]
