# Generated by Django 3.0.5 on 2020-05-11 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='item_json',
            field=models.CharField(default='', max_length=5000),
        ),
    ]
