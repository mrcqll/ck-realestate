"""Realtor authentication for the existing Django administration site."""
from functools import wraps

from django.contrib.admin import AdminSite
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth.views import LogoutView
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy


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

    def logout(self, request, extra_context=None):
        """End the session and return the Realtor to a clear public state."""
        return LogoutView.as_view(
            next_page=f"{reverse_lazy('home')}?logged_out=1",
            extra_context={
                **(extra_context or {}),
                "has_permission": False,
            },
        )(request)

    def admin_view(self, view, cacheable=False):
        protected_view = super().admin_view(view, cacheable=cacheable)

        @wraps(protected_view)
        def authorized_view(request, *args, **kwargs):
            if request.user.is_authenticated and not self.has_permission(request):
                raise PermissionDenied
            return protected_view(request, *args, **kwargs)

        return authorized_view
