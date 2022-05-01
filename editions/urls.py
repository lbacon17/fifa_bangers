from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.all_editions_and_years, name="editions"),
]
