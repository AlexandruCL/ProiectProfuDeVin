import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create/elevate a superuser from env vars (idempotent)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            default=os.environ.get("ADMIN_USERNAME")
            or os.environ.get("DJANGO_SUPERUSER_USERNAME"),
        )
        parser.add_argument(
            "--email",
            default=os.environ.get("ADMIN_EMAIL")
            or os.environ.get("DJANGO_SUPERUSER_EMAIL"),
        )
        parser.add_argument(
            "--password",
            default=os.environ.get("ADMIN_PASSWORD")
            or os.environ.get("DJANGO_SUPERUSER_PASSWORD"),
        )
        parser.add_argument(
            "--update-password",
            action="store_true",
            help="If user exists, update password from --password.",
        )

    def handle(self, *args, **options):
        username = options["username"]
        email = options["email"]
        password = options["password"]
        update_password = options["update_password"]

        if not username:
            raise RuntimeError(
                "Missing username. Set ADMIN_USERNAME (or DJANGO_SUPERUSER_USERNAME)."
            )
        if not password:
            raise RuntimeError(
                "Missing password. Set ADMIN_PASSWORD (or DJANGO_SUPERUSER_PASSWORD)."
            )

        User = get_user_model()

        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email or ""},
        )

        changed = False
        if created:
            user.is_staff = True
            user.is_superuser = True
            user.set_password(password)
            changed = True
        else:
            if not user.is_staff:
                user.is_staff = True
                changed = True
            if not user.is_superuser:
                user.is_superuser = True
                changed = True
            if update_password:
                user.set_password(password)
                changed = True

        if email and user.email != email:
            user.email = email
            changed = True

        if changed:
            user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f"Created superuser '{username}'."))
        else:
            self.stdout.write(
                self.style.WARNING(
                    f"Superuser '{username}' already exists (updated={changed})."
                )
            )
