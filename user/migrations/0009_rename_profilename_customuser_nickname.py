# Generated by Django 5.2 on 2025-04-28 08:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_alter_customuser_fcmtoken'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='profileName',
            new_name='nickname',
        ),
    ]
