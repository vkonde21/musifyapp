from rest_framework import serializers
from .models import Playlist, Song
class songlisting(serializers.RelatedField):
    def to_representation(self, data):
       return data.title


class playlistsongserializer(serializers.ModelSerializer):
    songs = songlisting(many = True, read_only=True)
    class Meta:
        model = Playlist
        fields = ['title','songs']
