"""Realtor authentication for the existing Django administration site."""
from functools import wraps

from django.contrib.admin import AdminSite
from django.contrib.admin.forms import AdminAuthenticationForm
from django.core.exceptions import PermissionDenied


class RealtorAuthenticationForm(AdminAuthenticationForm):
    error_messages = {
        **AdminAuthenticationForm.error_messages,
        "invalid_login": "Unable to sign in with those credentials.",
        "inactive": "Unable to sign in with those credentials.",
    }


class RealtorAdminSite(AdminSite):
    site_header = "CK Realestate Administration"
    site_title = "CK Realestate"
    login_form = RealtorAuthenticationForm
    login_template = "admin/realtor_login.html"

    def login(self, request, extra_context=None):
        return super().login(request, {
            **(extra_context or {}), "title": "Realtor Login",
        })

    def admin_view(self, view, cacheable=False):
        protected_view = super().admin_view(view, cacheable=cacheable)

        @wraps(protected_view)
        def authorized_view(request, *args, **kwargs):
            if request.user.is_authenticated and not self.has_permission(request):
                raise PermissionDenied
            return protected_view(request, *args, **kwargs)

        return authorized_view
