from django.contrib import admin
from django.urls import path, include
from . import views
from editions import views as v

urlpatterns = [path("", v.all_editions_and_years, name="home")]
