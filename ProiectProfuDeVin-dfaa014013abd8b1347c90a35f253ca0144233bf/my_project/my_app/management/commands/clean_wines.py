from django.core.management.base import BaseCommand
from django.db import connection
from my_app.models import Wines

class Command(BaseCommand):
    help = 'Clean all wines and reset the ID from 1'

    def handle(self, *args, **kwargs):
        Wines.objects.all().delete()
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='my_app_wines';")
        self.stdout.write(self.style.SUCCESS('All wines have been deleted and IDs reset'))