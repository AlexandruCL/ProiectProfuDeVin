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
    next_url = request.GET.get('next', 'home')
    logout(request)
    return redirect(next_url)

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
        messages.error(request, 'Not enough stock available.', extra_tags='cartadd-error')
        if(item_type == 'wine'):
            return redirect('wine_list')
        else:
            return redirect('spirit_list')

    # Get or create a cart for the user
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Get or create a cart item for the item
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        wine=item if item_type == 'wine' else None,
        spirit=item if item_type == 'spirit' else None
    )

    if not created and cart_item.quantity + quantity > item.Qty:
        messages.error(request, 'Cannot add more items than available in stock. Check your cart.', extra_tags='cartadd-error')
        if(item_type == 'wine'):
            return redirect('wine_list')
        else:
            return redirect('spirit_list')
    
    if created:
        cart_item.quantity = quantity
    else:
        cart_item.quantity += quantity
    cart_item.save()

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

    year_choices = Wines.objects.values_list('Year', flat=True).distinct().order_by('-Year')

    context = {
        'wines': wines,
        'search_query': search_query,
        'year_filter': year_filter,
        'year_choices': year_choices,
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
    next_url = request.GET.get('next', 'home')
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(next_url)
    else:
        form = CustomAuthenticationForm()
    return render(request, 'my_app/login.html', {'form': form, 'next': next_url})

def signup_view(request):
    next_url = request.GET.get('next', 'home')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(next_url)
        else:
            print(form.errors)  # Print form errors to the console for debugging
    else:
        form = CustomUserCreationForm()
    return render(request, 'my_app/signup.html', {'form': form, 'next': next_url})

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

    messages.success(request, 'Item removed from cart.', extra_tags='cartrmv-success')
    return redirect('cart_view')