from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Wines(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    grapes = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.IntegerField(null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    ID = models.AutoField(primary_key=True, editable=False)
    def __str__(self):
        return f'{self.name} | {self.year} | {self.grapes} | {self.country} | {self.region} | {self.description} | {self.quantity} | {self.price} | {self.ID}'

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Enforce unique constraint
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f'Cart of: {self.user}'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    wine = models.ForeignKey(Wines, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return f'{self.wine} | {self.quantity}'