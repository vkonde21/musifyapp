# Generated by Django 3.0.6 on 2020-07-16 03:57

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('playlist', '0007_auto_20200715_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 16, 3, 57, 42, 859152, tzinfo=utc)),
        ),
    ]
