from django import forms

from .models import Listing


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            "address",
            "price",
            "description",
            "features",
            "home_type",
            "neighborhood",
            "status",
            "photo_1",
            "photo_2",
            "photo_3",
            "photo_4",
        ]