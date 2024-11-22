from django.core.management.base import BaseCommand
from django.db import connection
from my_app.models import Spirits

class Command(BaseCommand):
    help = 'Clean all spirits and reset the ID from 1'

    def handle(self, *args, **kwargs):
        Spirits.objects.all().delete()
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='my_app_spirits';")
        self.stdout.write(self.style.SUCCESS('All spirits have been deleted and IDs reset'))