from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from my_app.models import Cart

class Command(BaseCommand):
    help = 'Clean up duplicate carts for each user'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        for user in users:
            carts = Cart.objects.filter(user=user)
            if carts.count() > 1:
                # Keep the first cart and delete the rest
                first_cart = carts.first()
                duplicate_carts = carts.exclude(id=first_cart.id)
                duplicate_carts.delete()
                self.stdout.write(self.style.SUCCESS(f'Deleted duplicate carts for user {user.username}'))
        self.stdout.write(self.style.SUCCESS('Cleanup completed'))