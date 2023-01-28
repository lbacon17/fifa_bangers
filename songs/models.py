from django.db import models
from django.core.files.storage import FileSystemStorage
from editions.models import Edition, Year
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating
from datetime import timedelta

# from django.contrib.postgres.fields import ArrayField


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, audio, max_length=None):
        self.delete(audio)
        return audio


class Song(models.Model):
    class Meta:
        verbose_name_plural = "Songs"

    edition = models.ForeignKey(
        Edition, null=False, blank=False, on_delete=models.CASCADE
    )
    title = models.CharField(max_length=254, null=False, blank=False)
    artist = models.CharField(max_length=100, null=False, blank=False, default="")
    album = models.CharField(max_length=100, null=True, blank=True, default="")
    audio = models.FileField(upload_to="audio", storage=OverwriteStorage())
    # duration = models.DurationField(default=timedelta(minutes=0, microseconds=0))
    thumbnail = models.ImageField(default="/song_thumbnails/music_icon.png")
    favourites = models.ManyToManyField(User, related_name="favourites", blank=True)
    rating = GenericRelation(Rating, related_query_name="songs")

    def __str__(self):
        return self.title


class Playlist(models.Model):
    class Meta:
        verbose_name_plural = "Playlists"

    songs = models.ManyToManyField(Song, related_name="songs")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    playlist_name = models.CharField(max_length=256)

    def __str__(self):
        return self.playlist_name
