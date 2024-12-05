# my_app/management/commands/reset_orders.py
from django.core.management.base import BaseCommand
from django.db import connection
from my_app.models import Order, OrderItem

class Command(BaseCommand):
    help = 'Delete all OrderItems and Orders, and reset the Order ID sequence'

    def handle(self, *args, **kwargs):
        # Delete all OrderItems
        OrderItem.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all OrderItems'))

        # Delete all Orders
        Order.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all Orders'))

        # Reset the Order ID sequence
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='my_app_order'")
        self.stdout.write(self.style.SUCCESS('Successfully reset the Order ID sequence'))