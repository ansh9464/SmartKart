# Generated by Django 3.0.8 on 2020-11-18 16:14

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_contactus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='chead2',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
