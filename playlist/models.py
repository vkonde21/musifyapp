from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

CHOICES = ((0, 'Private'),
                  (1, 'Public'),
                  (2, 'FollowersOnly'),
                  )
class Song(models.Model):
    sid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1000)
    artist = models.CharField(max_length=1000)
    mp3 = models.FileField('Track File',upload_to="track/")
    status = models.IntegerField(choices=CHOICES, default=0)
    date_added = models.DateTimeField(default=timezone.now(), blank=True, null=True)
    objects = models.Manager()
    def __str__(self):
        return self.title

class Playlist(models.Model):
    pid = models.AutoField(primary_key = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length = 1000)
    songs = models.ManyToManyField(Song)
    status = models.IntegerField(choices=CHOICES, default=0)
    logo = models.FileField()
    date_created = models.DateTimeField(default = timezone.now())
    objects = models.Manager()
    def __str__(self):
        return self.title

