from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Edition, Year
from .forms import EditionForm, YearForm


def all_editions_and_years(request):
    """Shows all editions and years"""
    editions = Edition.objects.all()
    years = Year.objects.all()

    # query = None
    # category = None
    # sort = None
    # direction = None

    template = "editions/editions.html"
    context = {
        "editions": editions,
        "years": years,
    }
    return render(request, template, context)


def get_edition(request, edition_id):
    edition = get_object_or_404(Edition, pk=edition_id)
    template = "editions/get_edition.html"
    context = {
        "edition": edition,
    }
    return render(request, template, context)


@login_required
def add_edition(request):
    if not request.user.is_superuser:
        messages.error(request, "Sorry, you don't have permission to access this page!")
        return redirect(reverse("home"))

    if request.method == "POST":
        form = EditionForm(request.POST, request.FILES)
        if form.is_valid():
            new_edition = form.save()
            messages.success(request, "Successfully created FIFA edition!")
            return redirect(reverse("get_edition", args=[new_edition.id]))
        else:
            messages.error(
                request,
                "Could not create edition. Please ensure you have filled out all fields correctly.",
            )
    else:
        form = EditionForm()

    template = "editions/add_edition.html"
    context = {
        "form": form,
    }
    return render(request, template, context)


def add_year(request):
    if not request.user.is_superuser:
        messages.error(request, "Sorry, that action is not permitted!")
        return redirect(reverse("home"))

    if request.method == "POST":
        form = YearForm(request.POST, request.FILES)
        if form.is_valid():
            edition = form.save()
            messages.success(request, "Successfully created FIFA edition!")
            return redirect(reverse("home"))
        else:
            messages.error(
                request,
                "Could not create edition. Please ensure you have filled out all fields correctly.",
            )
    else:
        form = YearForm()

    template = "editions/editions.html"
    context = {
        "form": form,
    }
    return render(request, template, context)
