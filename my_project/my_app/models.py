from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Wines(models.Model):
    Name = models.CharField(max_length=100)
    Type = models.CharField(max_length=100)
    Year = models.IntegerField(default=None, null=True)  # Changed to allow NULL or default value
    Grapes = models.CharField(max_length=100, default='')
    Country = models.CharField(max_length=100)
    Region = models.CharField(max_length=100, default='')
    Price = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    Description = models.TextField()
    Qty = models.IntegerField(null=True)  # Kept as is, can be set to default if needed
    ID = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return f'{self.ID} | {self.Name} | {self.Year} | {self.Country} | {self.Qty} '

class Spirits(models.Model):
    Type = models.CharField(max_length=100, default = '')
    Name = models.CharField(max_length=100)
    Style = models.CharField(max_length=100, default = '-')
    AlcLvl = models.DecimalField(max_digits=4, decimal_places=2)
    Price = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    Qty = models.IntegerField(null=True)
    ID = models.AutoField(primary_key=True, editable=False)
    def __str__(self):
        return f'{self.ID} | {self.Type} | {self.Name} | {self.Qty}'
    
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