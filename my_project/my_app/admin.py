from django.contrib import admin
from .models import Wines, Cart, CartItem, Spirits

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1

class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]

class WinesAdmin(admin.ModelAdmin):
    list_display = ('ID', 'Name', 'Type', 'Year', 'Price', 'Qty', 'image')  # Add 'image' here

class SpiritsAdmin(admin.ModelAdmin):
    list_display = ('ID', 'Name', 'Type', 'Price', 'Qty', 'image')  # Add 'image' here

admin.site.register(Wines, WinesAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)
admin.site.register(Spirits, SpiritsAdmin)