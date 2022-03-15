from django.shortcuts import render

"""
Returns the home page
"""


def index(request):
    return render(request, "home/index.html")
