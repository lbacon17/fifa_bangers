from django.db import models
from django.core.files.storage import FileSystemStorage
from editions.models import Edition, Year

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
    # featured_artists = ArrayField(
    #     models.CharField(max_length=100, null=True, blank=True),
    #     size=8,
    #     null=True,
    #     blank=True,
    #     default=[],
    # )
    album = models.CharField(max_length=100, null=True, blank=True, default="")
    audio = models.FileField(upload_to="audio", storage=OverwriteStorage())

    def __str__(self):
        return self.title
