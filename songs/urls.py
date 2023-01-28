from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.all_songs, name="songs"),
    path("<int:song_id>/", views.song_info, name="song_info"),
    path("search/", views.autocomplete, name="autocomplete"),
    path("add_song", views.add_song, name="add_song"),
    path("favourites/<int:song_id>", views.favourites, name="favourites"),
    path("user_favourites/", views.user_favourites, name="user_favourites"),
    path("playlists", views.user_playlists, name="playlists"),
    path("create_playlist", views.create_playlist, name="create_playlist"),
    path(
        "add_to_playlist/<int:song_id>", views.add_to_playlist, name="add_to_playlist"
    ),
    path("playlists/<int:playlist_id>", views.playlist_info, name="playlist_info"),
    path(
        "playlists/update/<int:playlist_id>",
        views.update_playlist_name,
        name="update_playlist_name",
    ),
    path(
        "playlists/manage/<int:playlist_id>",
        views.manage_playlist,
        name="manage_playlist",
    ),
    path(
        "playlists/<int:playlist_id>/songs/remove/<int:song_id>",
        views.remove_song_from_playlist,
        name="remove_song_from_playlist",
    ),
    path(
        "playlists/delete/<int:playlist_id>",
        views.delete_playlist,
        name="delete_playlist",
    ),
]
