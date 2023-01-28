from django import forms
from django.forms import formset_factory
from .models import Song, Playlist
from editions.models import Edition
from django.contrib.auth.models import User


class SongForm(forms.ModelForm):
    class Meta:

        model = Song
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        editions = Edition.objects.all()
        edition_names = [(edition.id, edition.__str__()) for edition in editions]
        self.fields["edition"].choices = edition_names


SongFormSet = formset_factory(SongForm, extra=2)


class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ("playlist_name", "songs")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
