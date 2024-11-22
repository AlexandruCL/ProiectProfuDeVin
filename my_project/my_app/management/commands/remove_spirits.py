# myapp/management/commands/depopulate_spirits.py
from django.core.management.base import BaseCommand
from my_app.models import Spirits

class Command(BaseCommand):
    help = 'Depopulate (delete) all records from the Spirits database'

    def handle(self, *args, **kwargs):
        # Deleting all entries in the Spirits table
        deleted_count, _ = Spirits.objects.all().delete()

        # Provide feedback on how many records were deleted
        if deleted_count > 0:
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted {deleted_count} spirits records.'))
        else:
            self.stdout.write(self.style.WARNING('No spirits records found to delete.'))
