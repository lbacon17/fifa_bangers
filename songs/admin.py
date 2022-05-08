from django.contrib import admin
from .models import Song


class SongAdmin(admin.ModelAdmin):
    list_display = (
        "edition",
        "title",
        "artist",
        "album",
        # "featured_artists",
        "audio",
    )


admin.site.register(Song, SongAdmin)
