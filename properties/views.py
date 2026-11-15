from django.http import HttpResponse
from django.urls import reverse


def home(request):
    return HttpResponse(
        "<h1>CK Realestate</h1><p>Local setup is working.</p>"
        f'<a href="{reverse("admin:login")}">Realtor Login</a>'
    )
