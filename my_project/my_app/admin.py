from django.contrib import admin
from .models import Wines, Cart, CartItem, Spirits

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1

class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]

admin.site.register(Wines)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)
admin.site.register(Spirits)
# Register your models here.
