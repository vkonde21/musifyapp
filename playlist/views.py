from django.shortcuts import render, redirect, HttpResponseRedirect
from playlist.forms import PlaylistForm, SongForm, UpdateSongForm, UpdatePlaylistForm
from .models import Playlist, Song
from login.models import Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.db.models import Q
import json
# Create your views here.
def homepage(request):
    return render(request, 'playlist/home.html')

@login_required
def createplaylist(request):
    if(request.method == "POST"):
        form = PlaylistForm(request.POST or None, request.FILES or None)
        p = Playlist.objects.filter(user = request.user)
        if form.is_valid():
            new = form.save(commit=False)
            new.user = request.user
            #Each playlist should have different title
            for play in p:
                if(play.title == new.title):
                    messages.warning(request, f"Playlist with {play.title} as title already exists!")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            new.save()
            messages.success(request, new.title + " playlist created successfully!!")
            return redirect("/home")
        else:
            messages.error(request, "playlist could not be created")
    else:
        
        form = PlaylistForm()
    return render(request, 'playlist/createplaylist.html', {'form': form})

def playlistid(id):
    q = Playlist.objects.filter(pid = id)
    return q[0]

def addsong(request, pk):
    if(request.method == "POST"):
        form = SongForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            #check audiofile extensions
            form.save(commit = False)
            x = Playlist.objects.get(pid = pk)
            s = Song(title = request.POST.get("title"), artist = request.POST.get("artist"), mp3 = request.FILES.get("mp3"), status = request.POST.get("status"))
            s.save()
            x.songs.add(s)
            messages.success(request, s.title +
                             " song added successfully!!")
            return redirect(f"/editplaylist/{pk}")
        else:
            messages.error(request, "playlist could not be created")
    else:
        form = SongForm()
        return render(request, "playlist/songform.html",{"form":form})

def updatesong(request, pid, pk):
    if(request.method == "POST"):
        s = Song.objects.get(sid=pk)
        form = UpdateSongForm(request.POST, request.FILES, instance = s)
        if form.is_valid():
            #check audiofile extensions
            x = form.save(commit=False)
            x.save()
            messages.success(request, x.title +
                             " song updated successfully!!")
            return redirect(f"/editplaylist/{pid}")
        else:
            messages.error(request, "Song could not be updated!!")
            return redirect(f"/editplaylist/{pid}")
    else:
        s = Song.objects.get(sid=pk)
        form = UpdateSongForm(instance = s )
        return render(request, "playlist/songform.html", {"form": form, "update":1})

def deletesong(request, pid, pk):
    x = Playlist.objects.get(pid = pid)
    k = Song.objects.filter(sid = pk)
    x.songs.remove(k[0])
    messages.success(request, f"{k[0].title} song successfully removed from {x.title} playlist!!")
    return redirect(f"/editplaylist/{pid}")

def deleteplaylist(request, pid):
    x = Playlist.objects.filter(pid = pid)
    title = x[0].title
    x[0].delete()
    messages.success(
        request, f"{title} playlist successfully deleted!!")
    return redirect(f"/home")

@login_required
def followuser(request, userid):
    u = User.objects.get(id = userid)
    #print(u)
    u.profile.followers.add(request.user)
    request.user.profile.following.add(u)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def unfollowuser(request, userid):
    u = User.objects.get(id=userid)
    #print(u)
    u.profile.followers.remove(request.user)
    request.user.profile.following.remove(u)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def userdashboard(request, userid):
    user = User.objects.get(id = userid)
    followers = user.profile.followers.all()
    p = Playlist.objects.filter(user__id = userid)
    playlistcount = p.count()
    pl = p.filter(status = 1)
    if(request.user in followers):
        pl = p.filter(Q(status = 1) | Q(status = 2))
    return render(request, "playlist/userdashboard.html", {"user":user, "playlists":pl, "plcount":playlistcount})

@login_required
def copysong(request, pid):
    #returns pid, lists of playlists, list of song for each playlist
    albumid = pid
    album = Playlist.objects.filter(pid = pid)
    playlists = Playlist.objects.filter(user = request.user).exclude(pid = pid)
    songdict = {}
    for p in playlists:
        l = []
        if(p.pid != pid):
            for k in p.songs.all():
                if(k not in album[0].songs.all()): #do not show list of songs which are already present in the current playlist
                    l.append([k.title, k.sid])
            songdict["playlist" + p.title] = l
    #songdict = str(songdict)
    #songdict = songdict.replace("'",'"')
    
    return render(request, "playlist/copysong.html", {"albumid":albumid, "playlists":playlists, "songdict":songdict, "copysong":1})


@login_required
def copysongtoplay(request, pid):
    l = [int(i) for i in request.POST.getlist("choices[]")] #id of songs to be copied
    p = Playlist.objects.get(pid = pid)
    for x in l:
        s = Song.objects.filter(sid = x)
        p.songs.add(s[0])
    messages.success(request, "Songs copied successfully")
    return redirect(f"/editplaylist/{pid}")
    #print(request.POST.get("category"))

@login_required
def transfersong(request, pid):
    albumid = pid
    playlists = Playlist.objects.filter(user = request.user).exclude(pid = pid)
    print(playlists)
    album = Playlist.objects.filter(pid=pid)
    songs = album[0].songs.all()
    return render(request, "playlist/transfersong.html", {"albumid": albumid, "playlists": playlists, "songs": songs, })


@login_required
def transfersongtoplay(request, pid):
    lp = [int(i) for i in request.POST.getlist(
        "choices[]")]  # id of playlists in which selected songs are to be copied
    print(lp)
    ls = [int(i) for i in request.POST.getlist("songs")]
    s = []
    for x in ls:
        q = Song.objects.get(sid = x)
        s.append(q)
    print(s)
    
    for p in lp:
        play = Playlist.objects.get(pid = p)
        for d in s:
            if(d not in play.songs.all()):
                play.songs.add(d)
            else:
                messages.warning(request, f"{d.title} song already present in current playlist!")
    #delete the song from current playlist
    for d in s:
        Playlist.objects.get(pid = pid).songs.remove(d)
    messages.success(request, "Songs transferred successfully")
    return redirect(f"/editplaylist/{pid}")


@login_required
def sortbydate(request, pid):
    songs = Playlist.objects.get(pid = pid).songs.all()
    songs = songs.order_by("-date_added")
    album = Playlist.objects.get(pid = pid)
    return render(request, "playlist/editplaylist.html", {"songs":songs, "album":album})

class Playlists(ListView):
    model = Playlist
    template_name = "playlist/home.html"
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = super(Playlists, self).get_queryset(*args, **kwargs)
        try:
            qs = qs.filter(user = self.request.user) #try is used in case of anonymous user
            qs = qs.order_by("-date_created")
        except:
            qs = []
        return qs

class EditPlaylist(ListView):
    model = Playlist
    template_name = "playlist/editplaylist.html"
    #context_object_name = 'songs'

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        data['songs'] = Playlist.objects.get(pid = self.kwargs['pk']).songs.all()
        data['album'] = playlistid(self.kwargs['pk'])
        return data

def searchuser(request):
    user = request.GET.get("searchuser")
    print(user)
    user = user.lower()
    qs = User.objects.filter(Q(username__icontains=user))
    following = request.user.profile.following.all()
    return render(request, "playlist/searchuser.html", {"users":qs, "following":following})
