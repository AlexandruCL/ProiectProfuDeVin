from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Wines(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100, default = '')
    year = models.IntegerField(null=True)
    grapes = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    quantity = models.IntegerField(null=True)
    ID = models.AutoField(primary_key=True, editable=False)
    def __str__(self):
        return f'{self.name} | {self.type} | {self.year} | {self.grapes} | {self.country} | {self.region} | {self.description} | {self.price} | {self.quantity} | {self.ID}'
    
class Spirits(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100, default = '')
    style = models.CharField(max_length=100, default = '')
    alclvl = models.DecimalField(max_digits=4, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    quantity = models.IntegerField(null=True)
    ID = models.AutoField(primary_key=True, editable=False)
    def __str__(self):
        return f'{self.name} | {self.type} | {self.style} | {self.alclvl} | {self.price} | {self.quantity} | {self.ID}'
    
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