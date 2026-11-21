from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ListingForm


def home(request):
    return HttpResponse(
        "<h1>CK Realestate</h1><p>Local setup is working.</p>"
        f'<a href="{reverse("admin:login")}">Realtor Login</a>'
    )


@staff_member_required
def add_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Listing added successfully.")
            return redirect("add_listing")
    else:
        form = ListingForm()
    return render(request, "properties/add_listing.html", {"form": form})