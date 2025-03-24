# Generated by Django 5.0.6 on 2025-03-24 18:01

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Response',
            new_name='ResponseText',
        ),
        migrations.RenameField(
            model_name='choiceanswer',
            old_name='response',
            new_name='ResponseText',
        ),
        migrations.RenameField(
            model_name='fileanswer',
            old_name='response',
            new_name='ResponseText',
        ),
        migrations.RenameField(
            model_name='rangeanswer',
            old_name='response',
            new_name='ResponseText',
        ),
        migrations.RenameField(
            model_name='textanswer',
            old_name='response',
            new_name='ResponseText',
        ),
    ]
