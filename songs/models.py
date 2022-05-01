from django.db import models
from editions.models import Edition, Year

# from django.contrib.postgres.fields import ArrayField


class Song(models.Model):
    class Meta:
        verbose_name_plural = "Songs"

    edition = models.ForeignKey(
        Edition, null=False, blank=False, on_delete=models.CASCADE
    )
    year = models.ForeignKey(
        Year,
        null=False,
        blank=False,
        default=1994,
        on_delete=models.CASCADE,
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
    audio = models.FileField(upload_to="media/audio", default="")

    def __str__(self):
        return self.title
