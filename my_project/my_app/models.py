from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Wines(models.Model):
    Name = models.CharField(max_length=100)
    Type = models.CharField(max_length=100)
    Year = models.IntegerField(default=None, null=True)  # Changed to allow NULL or default value
    Grapes = models.CharField(max_length=100, null=True)  # Changed to allow NULL
    Country = models.CharField(max_length=100)
    Region = models.CharField(max_length=100, null=True)  # Changed to allow NULL
    Price = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    Description = models.TextField()
    Qty = models.IntegerField(null=True)  # Kept as is, can be set to default if needed
    ID = models.AutoField(primary_key=True, editable=False)
    image = models.ImageField(upload_to='wines/', null=True, blank=True)  # Add this line

    def __str__(self):
        return f'{self.ID} | {self.Name} | {self.Year} | {self.Price} | {self.Qty} '

class Spirits(models.Model):
    Type = models.CharField(max_length=100, default = '')
    Name = models.CharField(max_length=100, default='')
    Style = models.CharField(max_length=100, null=True)
    AlcLvl = models.IntegerField(default=0)
    Price = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    Qty = models.IntegerField(null=True)
    ID = models.AutoField(primary_key=True, editable=False)
    image = models.ImageField(upload_to='spirits/', null=True, blank=True)  # Add this line
    def __str__(self):
        return f'{self.ID} | {self.Type} | {self.Name} | {self.Price} | {self.Qty}'
    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Enforce unique constraint
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f'Cart of: {self.user}'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    wine = models.ForeignKey(Wines, null=True, blank=True, on_delete=models.CASCADE)
    spirit = models.ForeignKey(Spirits, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, default=0.00)
    def __str__(self):
        return f'{self.wine or self.spirit} | {self.quantity}'
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    first_name = models.CharField(max_length=30,default='')
    last_name = models.CharField(max_length=30,default='')
    email = models.EmailField(max_length=254, default='')
    phone_number = models.CharField(max_length=15, default='')
    address = models.CharField(max_length=255 , null=True)
    city = models.CharField(max_length=100, null=True)
    county = models.CharField(max_length=100, default='')
    postal_code = models.CharField(max_length=6, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'
    
    def get_order_items(self):
        return OrderItem.objects.filter(order=self)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    wine = models.ForeignKey(Wines, null=True, blank=True, on_delete=models.CASCADE)
    spirit = models.ForeignKey(Spirits, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    name = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    grapes = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    alcohol_level = models.IntegerField(null=True, blank=True)
    style = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.name} | {self.quantity}'