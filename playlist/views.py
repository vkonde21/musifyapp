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
# Create your views here.
def homepage(request):
    return render(request, 'playlist/home.html')

@login_required
def createplaylist(request):
    if(request.method == "POST"):
        form = PlaylistForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            new = form.save(commit=False)
            new.user = request.user
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
