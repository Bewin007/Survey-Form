# Generated by Django 5.0.6 on 2025-03-24 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_rename_response_responsetext_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileupload',
            name='file_upload',
            field=models.FileField(default=1, upload_to='uploads/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='specialfield',
            name='special_field',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='rangefield',
            name='end',
            field=models.FloatField(default=10),
        ),
    ]
