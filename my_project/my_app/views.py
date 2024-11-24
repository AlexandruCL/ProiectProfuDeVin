from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Wines, Cart, CartItem, Spirits
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm


@login_required
def add_to_cart(request, item_id, item_type):
    if item_type == 'wine':
        item = get_object_or_404(Wines, ID=item_id)
    elif item_type == 'spirit':
        item = get_object_or_404(Spirits, ID=item_id)
    else:
        messages.error(request, 'Invalid item type.')
        return redirect('drinks_list')

    quantity = int(request.POST.get('quantity', 1))
    
    if item.Qty < quantity:
        messages.error(request, 'Not enough stock available.')
        return redirect('drinks_list')

    # Get or create a cart for the user
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Get or create a cart item for the item
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        wine=item if item_type == 'wine' else None,
        spirit=item if item_type == 'spirit' else None
    )
    if created:
        cart_item.quantity = quantity
    else:
        cart_item.quantity += quantity
    cart_item.save()

    # Decrease the quantity of the item in stock
    item.Qty -= quantity
    item.save()

    return redirect('drinks_list')



def drinks_list(request):
    wines = Wines.objects.all()
    spirits = Spirits.objects.all()
    return render(request, 'my_app/drinks_list.html', {'wines': wines, 'spirits': spirits})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('drinks_list')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'my_app/login.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('drinks_list')
        else:
            print(form.errors)  # Print form errors to the console for debugging
    else:
        form = CustomUserCreationForm()
    return render(request, 'my_app/signup.html', {'form': form})