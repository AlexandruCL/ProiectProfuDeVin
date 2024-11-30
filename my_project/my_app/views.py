from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Wines, Cart, CartItem, Spirits
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import logout
from django.views.decorators.http import require_POST

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def add_to_cart(request, item_id, item_type):
    if item_type == 'wine':
        item = get_object_or_404(Wines, ID=item_id)
    elif item_type == 'spirit':
        item = get_object_or_404(Spirits, ID=item_id)
    else:
        messages.error(request, 'Invalid item type.')
        return redirect('home')

    quantity = int(request.POST.get('quantity', 1))
    
    if item.Qty < quantity:
        messages.error(request, 'Not enough stock available.')
        return redirect('home')

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
    item.Qty -= quantity #Quantity should decrese only after a order is placed, we will change this later
    item.save()
    if(item_type == 'wine'):
        return redirect('wine_list')
    elif(item_type == 'spirit'):
        return redirect('spirit_list')
    else:
        return redirect('home')

def wine_list(request):
    wines = Wines.objects.all()
    search_query = request.GET.get('search', '')
    year_filter = request.GET.get('year', '')

    if search_query:
        wines = wines.filter(Name__icontains=search_query)
    
    if year_filter:
        wines = wines.filter(Year=year_filter)

    context = {
        'wines': wines,
        'search_query': search_query,
        'year_filter': year_filter,
    }
    return render(request, 'my_app/wine_list.html', context)

def spirit_list(request):
    spirits = Spirits.objects.all()
    return render(request, 'my_app/spirit_list.html', {'spirits': spirits})

def home(request):
    return render(request, 'my_app/home.html')

def product_list(request):
    return render(request, 'my_app/product_list.html')

def contact(request):
    return render(request, 'my_app/contact.html')

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'my_app/login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            print(form.errors)  # Print form errors to the console for debugging
    else:
        form = CustomUserCreationForm()
    return render(request, 'my_app/signup.html', {'form': form})

login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'my_app/cart.html', {'cart_items': cart_items})

@require_POST
@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity_to_remove = int(request.POST.get('quantity', 1))

    if quantity_to_remove >= cart_item.quantity:
        cart_item.delete()
    else:
        cart_item.quantity -= quantity_to_remove
        cart_item.save()

    messages.success(request, 'Item removed from cart.')
    return redirect('cart_view')