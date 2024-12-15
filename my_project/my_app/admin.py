from django.contrib import admin
from .models import Wines, Cart, CartItem, Spirits, Order, OrderItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]

class WinesAdmin(admin.ModelAdmin):
    list_display = ('ID', 'Name', 'Type', 'Year', 'Price', 'Qty', 'image')  # Add 'image' here

class SpiritsAdmin(admin.ModelAdmin):
    list_display = ('ID', 'Name', 'Type', 'Price', 'Qty', 'image')  # Add 'image' here

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  # Do not show extra empty forms

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'first_name', 'last_name','email', 'phone_number', 'address', 'city', 'county', 'postal_code', 'total_price', 'status')
    search_fields = ('user__username', 'first_name', 'last_name','email', 'phone_number', 'address', 'city', 'county', 'postal_code')
    list_filter = ('created_at', 'city', 'county', 'status')
    inlines = [OrderItemInline]

admin.site.register(Wines, WinesAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)
admin.site.register(Spirits, SpiritsAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)