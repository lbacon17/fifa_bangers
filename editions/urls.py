from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.all_editions_and_years, name="editions"),
    path("<int:edition_id>/", views.get_edition, name="get_edition"),
    path("add_edition/", views.add_edition, name="add_edition"),
]
