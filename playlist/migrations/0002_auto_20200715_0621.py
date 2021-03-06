# Generated by Django 3.0.6 on 2020-07-15 06:21

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('playlist', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 15, 6, 21, 52, 868800, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='song',
            name='mp3',
            field=models.FileField(upload_to='track/', verbose_name='Track File'),
        ),
    ]
