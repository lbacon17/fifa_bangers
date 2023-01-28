from django.shortcuts import render, get_object_or_404
from .models import UserProfile
from django.contrib.auth.models import User


def profile(request, user_id, username):
    profile = get_object_or_404(User, id=user_id)
    username = User.objects.filter(username=username)
    template = "profiles/profile.html"
    return render(request, template)
