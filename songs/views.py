from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .models import Song


def all_songs(request):
    songs = Song.objects.all()
    return render(request, "songs/songs.html")


# Create your views here.
