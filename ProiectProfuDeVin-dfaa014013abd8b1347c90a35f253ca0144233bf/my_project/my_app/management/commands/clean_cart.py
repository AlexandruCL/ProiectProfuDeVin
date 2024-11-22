from django.core.management.base import BaseCommand
from my_app.models import Cart, CartItem

class Command(BaseCommand):
    help = 'Delete all items in Cart and CartItem'

    def handle(self, *args, **kwargs):
        CartItem.objects.all().delete()
        Cart.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All items in Cart and CartItem have been deleted'))