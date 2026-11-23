import os

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import Permission
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction


class Command(BaseCommand):
    help = "Create the dedicated demo realtor with listing permissions."

    @transaction.atomic
    def handle(self, *args, **options):
        username = os.getenv("DEMO_REALTOR_USERNAME", "")
        password = os.getenv("DEMO_REALTOR_PASSWORD", "")
        if not username or not password:
            raise CommandError("Set DEMO_REALTOR_USERNAME and DEMO_REALTOR_PASSWORD.")

        user_model = get_user_model()
        account = user_model(username=username, is_active=True, is_staff=True)
        try:
            user_model._meta.get_field("username").clean(username, account)
        except ValidationError:
            raise CommandError("The demo username is invalid.") from None

        permissions = set(Permission.objects.filter(
            content_type__app_label="properties",
            content_type__model="listing",
            codename__in=("view_listing", "add_listing", "change_listing", "delete_listing"),
        ))
        if len(permissions) != 4:
            raise CommandError("Run migrations before seeding the demo realtor.")

        def initial_password():
            try:
                validate_password(password, account)
            except ValidationError:
                raise CommandError("The demo password failed Django password validation.") from None
            return make_password(password)

        user, created = user_model.objects.get_or_create(
            username=username,
            defaults={"password": initial_password, "is_active": True, "is_staff": True},
        )
        if created:
            user.user_permissions.set(permissions)
            self.stdout.write("Demo realtor created.")
            return

        if (
            not user.is_active or not user.is_staff or user.is_superuser
            or user.groups.exists() or set(user.user_permissions.all()) != permissions
            or not check_password(password, user.password)
        ):
            raise CommandError("The existing account does not match the configured demo realtor.")
        self.stdout.write("Demo realtor already configured.")
