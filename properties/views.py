from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.static import serve

from .forms import ListingForm


def home(request):
    logout_message = (
        "<p role=\"status\">You have been logged out.</p>"
        if request.GET.get("logged_out") == "1"
        else ""
    )
    return HttpResponse(
        "<h1>CK Realestate</h1><p>Local setup is working.</p>"
        f"{logout_message}"
        f'<a href="{reverse("admin:login")}">Realtor Login</a>'
    )


@staff_member_required
@permission_required("properties.add_listing", raise_exception=True)
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


@staff_member_required
@permission_required("properties.view_listing", raise_exception=True)
def listing_media(request, path):
    return serve(request, path, document_root=settings.MEDIA_ROOT, show_indexes=False)
