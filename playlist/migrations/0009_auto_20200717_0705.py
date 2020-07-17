# Generated by Django 3.0.6 on 2020-07-17 07:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('playlist', '0008_auto_20200716_0357'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='date_added',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 7, 17, 7, 5, 23, 665721, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 17, 7, 5, 23, 666415, tzinfo=utc)),
        ),
    ]
