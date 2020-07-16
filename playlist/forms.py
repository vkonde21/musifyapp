from .models import Playlist, Song
from django import forms
class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['title','logo','status']

class UpdatePlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['title', 'logo', 'status']

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'artist', 'status', 'mp3']

class UpdateSongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'artist', 'status', 'mp3']
