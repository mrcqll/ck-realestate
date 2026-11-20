from django.http import HttpResponse
from django.urls import reverse


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
