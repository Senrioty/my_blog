# Generated by Django 2.0.13 on 2019-09-19 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0006_auto_20190914_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='likes',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
