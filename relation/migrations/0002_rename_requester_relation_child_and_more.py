# Generated by Django 5.2 on 2025-04-24 03:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relation', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='relation',
            old_name='requester',
            new_name='child',
        ),
        migrations.RenameField(
            model_name='relation',
            old_name='target_name',
            new_name='childName',
        ),
        migrations.RenameField(
            model_name='relation',
            old_name='target_phone',
            new_name='parentName',
        ),
        migrations.AlterUniqueTogether(
            name='relation',
            unique_together={('child', 'parentName')},
        ),
        migrations.AddField(
            model_name='relation',
            name='parent_user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='target', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
