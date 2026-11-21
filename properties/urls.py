from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("listings/add/", views.add_listing, name="add_listing"),
]