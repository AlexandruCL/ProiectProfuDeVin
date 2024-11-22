from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Wines, Cart, CartItem, Spirits
from django.contrib import messages


@login_required
def add_to_cart(request, wine_id):
    wine = get_object_or_404(Wines, ID=wine_id)
    quantity = int(request.POST.get('quantity', 1))
    
    if wine.quantity < quantity:
        # Handle the case where there is not enough stock
        return redirect('wine_list')  # Redirect to the wine list view or any other view with an error message
        messages.error(request, 'Not enough stock available.')

    # Get or create a cart for the user
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Get or create a cart item for the wine
    cart_item, created = CartItem.objects.get_or_create(cart=cart, wine=wine)
    if created:
        cart_item.quantity = quantity
    else:
        cart_item.quantity += quantity
    cart_item.save()

    # Decrease the quantity of the wine in stock
    wine.quantity -= quantity
    wine.save()

    return redirect('wine_list')

def wine_list(request):
    wines = Wines.objects.all()
    return render(request, 'my_app/wine_list.html', {'wines': wines})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('wine_list')
    else:
        form = AuthenticationForm()
    return render(request, 'my_app/login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('wine_list')
    else:
        form = UserCreationForm()
    return render(request, 'my_app/signup.html', {'form': form})