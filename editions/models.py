from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime


class Year(models.Model):
    class Meta:
        verbose_name_plural = "Years"

    year = models.IntegerField(
        validators=[
            MaxValueValidator(datetime.datetime.now().year),
            MinValueValidator(1994),
        ]
    )
    short_year = models.CharField(max_length=4)

    def __str__(self):
        return str(self.year)

    def get_short_year(self):
        return str(self.short_year)


class Edition(models.Model):
    year = models.ForeignKey(
        Year,
        null=False,
        blank=False,
        default=1994,
        on_delete=models.CASCADE,
    )
    edition_name = models.CharField(max_length=30, null=False, blank=False)
    release_date = models.DateField(null=True, blank=True)
    publisher = models.CharField(max_length=254)
    cover = models.ImageField(null=True, blank=True)
    cover_image_url = models.URLField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return self.edition_name
