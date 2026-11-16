from django.contrib.admin.apps import AdminConfig


class RealtorAdminConfig(AdminConfig):
    default_site = "config.admin.RealtorAdminSite"
