from django.contrib import admin
from .models import Song, Playlist


class SongAdmin(admin.ModelAdmin):
    list_display = (
        "edition",
        "title",
        "artist",
        "album",
        "audio",
        "thumbnail",
    )

    ordering = ("edition",)


class PlaylistAdmin(admin.ModelAdmin):
    list_display = (
        "playlist_name",
        "user",
    )


admin.site.register(Song, SongAdmin)
admin.site.register(Playlist, PlaylistAdmin)
