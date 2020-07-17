from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import updateplaylist,playsonglist, sortbydate, sortbyartist, sortbytitle, ViewPlaylist, homepage, createplaylist, Playlists, EditPlaylist, addsong, updatesong, deletesong, deleteplaylist, searchuser, followuser, unfollowuser, userdashboard, copysong, transfersong, copysongtoplay, transfersongtoplay
app_name = "playlist"
urlpatterns = [
    path('home/', Playlists.as_view(), name="home" ),
    path('createplaylist/', createplaylist, name="playlist"),
    path('editplaylist/<int:pk>', EditPlaylist.as_view(), name="edit"),
    path('addsong/<int:pk>', addsong , name="addsong"),
    path('updatesong/<int:pid>/<int:pk>', updatesong, name="updatesong"),
    path('updateplaylist/<int:pid>', updateplaylist, name="updateplaylist"),
    path('deletesong/<int:pid>/<int:pk>', deletesong, name="deletesong"),
    path('deleteplaylist/<int:pid>', deleteplaylist, name="deleteplaylist"),
    path('searchuser', searchuser, name="searchuser"),
    path('follow/<int:userid>', followuser, name="followuser"),
    path('unfollow/<int:userid>', unfollowuser, name="unfollowuser"),
    path('userdashboard/<int:userid>', userdashboard, name="userdahboard"),
    path("copysong/<int:pid>", copysong, name="copysong"),
    path("transfersong/<int:pid>", transfersong, name="transfersong"),
    path("copysongtoplay/<int:pid>", copysongtoplay, name="copysongtoplay"),
    path("transfersongtoplay/<int:pid>", transfersongtoplay, name="transfersongtoplay"),
    path("sortbydate/<int:pid>", sortbydate, name="sortbydate"),
    path("sortbyartist/<int:pid>", sortbyartist, name="sortbyartist"),
    path("sortbytitle/<int:pid>", sortbytitle, name="sortbytitles"),
    path("detailview/<int:userid>/<int:pk>",ViewPlaylist.as_view(), name="viewdetails"),
    path("playlists/", playsonglist.as_view(), name="playlists")

]
