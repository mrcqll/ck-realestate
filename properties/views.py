from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def home(request):
    return HttpResponse(
        "<h1>CK Realestate</h1><p>Local setup is working.</p>"
    )