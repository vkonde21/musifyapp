from django.urls import path
from .views import homepage, createplaylist, Playlists, EditPlaylist, addsong, updatesong, deletesong, deleteplaylist, searchuser, followuser, unfollowuser, userdashboard
app_name = "playlist"
urlpatterns = [
    path('home/', Playlists.as_view(), name="home" ),
    path('createplaylist/', createplaylist, name="playlist"),
    path('editplaylist/<int:pk>', EditPlaylist.as_view(), name="edit"),
    path('addsong/<int:pk>', addsong , name="addsong"),
    path('updatesong/<int:pid>/<int:pk>', updatesong, name="updatesong"),
    path('deletesong/<int:pid>/<int:pk>', deletesong, name="deletesong"),
    path('deleteplaylist/<int:pid>', deleteplaylist, name="deleteplaylist"),
    path('searchuser', searchuser, name="searchuser"),
    path('follow/<int:userid>', followuser, name="followuser"),
    path('unfollow/<int:userid>', unfollowuser, name="unfollowuser"),
    path('userdashboard/<int:userid>', userdashboard, name="userdahboard")

]
