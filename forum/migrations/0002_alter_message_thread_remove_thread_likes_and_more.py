# Generated by Django 5.1.1 on 2024-09-27 13:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='thread',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.thread'),
        ),
        migrations.RemoveField(
            model_name='thread',
            name='likes',
        ),
        migrations.AddField(
            model_name='thread',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='thread_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
