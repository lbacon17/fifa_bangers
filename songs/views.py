from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg
from django.db.models.functions import Lower
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from .models import Song, Playlist
from .forms import SongForm, SongFormSet, PlaylistForm
import json
from random import shuffle


def all_songs(request):
    songs = Song.objects.all()
    query = None
    sort = None
    direction = None

    if request.GET:
        # checks whether a sort parameter exists and orders by selected
        # criteria if so
        if "sort" in request.GET:
            sortkey = request.GET["sort"]
            sort = sortkey
            if sortkey == "title":
                sortkey == "lower_title"
                songs = songs.annotate(lower_title=Lower("title"))
            if sortkey == "artist":
                sortkey == "lower_artist"
                songs = songs.annotate(lower_artist=Lower("artist"))
            if sortkey == "edition":
                sortkey = "edition__year"
            if "direction" in request.GET:
                direction = request.GET["direction"]
                if direction == "desc":
                    sortkey = f"-{sortkey}"
            songs = songs.order_by(sortkey)

        # checks whether search query exists and returns results containing
        # keywords
        if "q" in request.GET:
            query = request.GET["q"]
            if not query:
                messages.error(request, "You didn't enter any search terms!")
                return redirect(reverse("songs"))
            if " - " in query:
                query_artist = query.split(" - ")[0]
                query_song = query.split(" - ")[-1]
                print(Q(artist__icontains=query))
                queries = Q(artist__icontains=query_artist) & Q(
                    title__icontains=query_song
                )
                songs = songs.filter(queries)
            else:
                queries = Q(title__icontains=query) | Q(artist__icontains=query)
                songs = songs.filter(queries)

    current_sorting = f"{sort}_{direction}"

    context = {
        "songs": songs,
        "search_term": query,
        "current_sorting": current_sorting,
    }
    template = "songs/songs.html"
    return render(request, template, context)


def autocomplete(request):
    mime_type = "application/json"
    if request.accepts(mime_type):
        query = request.GET.get("term", "")
        queries = Q(title__icontains=query) | Q(artist__icontains=query)
        songs = Song.objects.filter(queries)
        search_suggestions = []
        for song in songs:
            place_json = song.artist + " - " + song.title
            search_suggestions.append(place_json)
        data = json.dumps(search_suggestions)
    return HttpResponse(data, mime_type)


@login_required
def add_song(request):
    if request.user.is_superuser:
        if request.method == "POST":
            form = SongForm(request.POST, request.FILES)
            if form.is_valid():
                new_song = form.save()
                messages.success(request, "Successfully added song.")
                if "another" in request.POST:
                    return redirect(reverse("add_song"))
                return redirect(reverse("songs"))
            else:
                messages.error(
                    request,
                    "Song could not be added. Please ensure the information has been entered correctly.",
                )
        else:
            form = SongForm()
    else:
        messages.error(
            request, "Sorry, you do not have permission to perform this action."
        )
        return redirect(reverse("home"))
    template = "songs/add_song.html"
    context = {
        "form": form,
    }
    return render(request, template, context)


def song_info(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    is_favourite = False
    if song.favourites.filter(id=request.user.id).exists():
        is_favourite = True

    template = "songs/song_info.html"
    context = {
        "song": song,
        "is_favourite": is_favourite,
    }
    return render(request, template, context)


@login_required
def favourites(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    if request.user.is_authenticated:
        if song.favourites.filter(id=request.user.id).exists():
            song.favourites.remove(request.user)
            return redirect(reverse("song_info", args=[song.id]))
        else:
            song.favourites.add(request.user)
            return redirect(reverse("song_info", args=[song.id]))

    messages.error(request, "Sorry, you must be logged in to perform that action!")
    raise PermissionDenied


@login_required
def user_favourites(request):
    user = request.user
    favourite_songs = user.favourites.all()
    template = "songs/favourites.html"
    context = {"favourite_songs": favourite_songs}
    return render(request, template, context)


@login_required
def user_playlists(request):
    if not request.user.is_authenticated:
        messages.error(request, "Please log in to view this page!")
        return redirect(reverse("home"))
    playlists = Playlist.objects.filter(user=request.user)
    template = "songs/playlists.html"
    context = {"playlists": playlists}
    return render(request, template, context)


@login_required
def create_playlist(request):
    songs = Song.objects.all()
    if request.method == "POST":
        form = PlaylistForm(request.POST, request.FILES)
        if form.is_valid():
            playlist = Playlist()
            playlist.playlist_name = request.POST["playlist_name"]
            playlist.user = request.user
            current_user_playlists = Playlist.objects.filter(user=request.user)
            selected_songs = request.POST["songs"]
            print(selected_songs)
            for x in current_user_playlists:
                if (
                    playlist.playlist_name.lower().strip()
                    == x.playlist_name.lower().strip()
                ):
                    print("Same name!")
                    messages.error(
                        request, "You already have a playlist with that name!"
                    )
                    return redirect(reverse("create_playlist"))
            playlist.save()
            playlist.songs.add(selected_songs)
            messages.success(
                request, f"Successfully created playlist {playlist.playlist_name}."
            )
            return redirect(reverse("playlists"))
        else:
            messages.error(
                request,
                "Playlist could not be created. Please ensure you have filled out all fields correctly.",
            )
    else:
        form = PlaylistForm()

    template = "songs/create_playlist.html"
    context = {"songs": songs, "form": form}
    return render(request, template, context)


@login_required
def add_to_playlist(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    playlists = Playlist.objects.filter(user=request.user)
    if request.method == "POST":
        for playlist in playlists:
            if playlist.user != request.user:
                raise PermissionDenied
            if playlist.playlist_name in request.POST:
                if song in playlist.songs.all():
                    messages.error(request, "Song is already in this playlist!")
                    return redirect(reverse("add_to_playlist", args=[song.id]))
                playlist.songs.add(song)
                messages.success(
                    request,
                    f"Successfully added {song.title} to playlist {playlist.playlist_name}!",
                )
        return redirect(reverse("song_info", args=[song.id]))

    template = "songs/add_to_playlist.html"
    context = {"playlists": playlists, "song": song}
    return render(request, template, context)


@login_required
def playlist_info(request, playlist_id):
    sort = None
    direction = None
    playlist = get_object_or_404(Playlist, pk=playlist_id)
    songs = playlist.songs.all()

    if playlist.user == request.user:
        if request.GET:
            if "sort" in request.GET:
                sortkey = request.GET["sort"]
                sort = sortkey
                if sortkey == "rating":
                    sortkey = "rating__average"
                if "direction" in request.GET:
                    direction = request.GET["direction"]
                    if direction == "desc":
                        sortkey = f"-{sortkey}"
                if sortkey == "shuffle":
                    songs = list(songs)
                    shuffle(songs)
                else:
                    songs = songs.order_by(sortkey)

        current_sorting = f"{sort}_{direction}" if sort != "shuffle" else f"{sort}"
        template = "songs/playlist_info.html"
        context = {
            "playlist": playlist,
            "songs": songs,
            "current_sorting": current_sorting,
        }
        return render(request, template, context)

    raise PermissionDenied


@login_required
def update_playlist_name(request, playlist_id):
    playlist = get_object_or_404(Playlist, pk=playlist_id)
    if playlist.user == request.user:
        if request.method == "POST":
            new_name = request.POST["playlist_name"]
            playlist.playlist_name = new_name
            playlist.save()
            messages.success(request, f"Updated playlist name to {new_name}.")
            return redirect(reverse("manage_playlist", args=[playlist.id]))
        template = "songs/edit_playlist.html"
        context = {"playlist": playlist}
        return render(request, template, context)
    raise PermissionDenied


@login_required
def manage_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, pk=playlist_id)
    songs = playlist.songs.all()
    all_songs = Song.objects.exclude(id__in=songs)
    paginator = Paginator(all_songs, 12)
    page_num = request.GET.get("page")
    page_obj = paginator.get_page(page_num)
    if playlist.user == request.user:
        if request.method == "POST":
            # song_search = request.POST["qq"]
            # if song_search:
            #     print(song_search)
            #     song_searches = Q(title__icontains=song_search) | Q(
            #         artist__icontains=song_search
            #     )
            #     all_songs = all_songs.filter(song_searches)
            #     return all_songs
            for song in all_songs:
                if song.title in request.POST:
                    playlist.songs.add(song)
                    messages.success(
                        request,
                        f"Successfully added {song.title} to playlist {playlist.playlist_name}.",
                    )
            return redirect(reverse("playlist_info", args=[playlist.id]))
        template = "songs/edit_playlist.html"
        context = {
            "playlist": playlist,
            "songs": songs,
            "all_songs": all_songs,
            "page_obj": page_obj,
        }
        return render(request, template, context)

    raise PermissionDenied


@login_required
def remove_song_from_playlist(request, playlist_id, song_id):
    playlist = get_object_or_404(Playlist, pk=playlist_id)
    song = get_object_or_404(Song, pk=song_id)
    songs = playlist.songs.all()
    if playlist.user == request.user:
        playlist.songs.remove(song)
        messages.success(
            request,
            f"Successfully removed {song.title} from playlist {playlist.playlist_name}.",
        )
        return redirect(reverse("playlist_info", args=[playlist.id]))

    raise PermissionDenied


@login_required
def delete_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, pk=playlist_id)
    if playlist.user == request.user:
        playlist.delete()
        messages.success(
            request, f"Successfully deleted playlist {playlist.playlist_name}."
        )
        return redirect(reverse("playlists"))

    raise PermissionDenied
