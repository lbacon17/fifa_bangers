from django.contrib import admin
from .models import Edition, Year
import datetime


class EditionAdmin(admin.ModelAdmin):
    list_display = (
        "year",
        "edition_name",
        "release_date",
        "publisher",
        "cover",
        "cover_image_url",
    )

    ordering = ("year",)


class YearAdmin(admin.ModelAdmin):
    list_display = ("year", "short_year")

    def save_model(self, request, obj, form, change):
        years = Year.objects.all()
        year_range = range(1994, datetime.datetime.now().year + 1)
        obj.save()
        for y in year_range:
            Year.objects.update_or_create(year=y, short_year=str(y)[-2:])
            year = Year.objects.filter(year=y)
            if year.count() > 1:
                for year in Year.objects.values_list().distinct():
                    Year.objects.filter(
                        pk__in=Year.objects.filter(year=y).values_list("id", flat=True)[
                            1:
                        ]
                    ).delete()


admin.site.register(Edition, EditionAdmin)
admin.site.register(Year, YearAdmin)
