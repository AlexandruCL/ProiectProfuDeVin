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
    type_filter = request.GET.get('type', '')
    country_filter = request.GET.get('country', '')
    region_filter = request.GET.get('region', '')
    grapes_filter = request.GET.get('grapes', '')
    sort_by = request.GET.get('sort_by', '')

    if search_query:
        wines = wines.filter(Name__icontains=search_query)
    
    if year_filter:
        wines = wines.filter(Year=year_filter)

    if type_filter:
        wines = wines.filter(Type__icontains=type_filter)
    
    if country_filter:
        wines = wines.filter(Country__icontains=country_filter)
    
    if region_filter:
        wines = wines.filter(Region__icontains=region_filter)
    
    if grapes_filter:
        wines = wines.filter(Grapes__icontains=grapes_filter)
    
    if sort_by == 'price_asc':
        wines = wines.order_by('Price')
    elif sort_by == 'price_desc':
        wines = wines.order_by('-Price')

    year_choices = Wines.objects.values_list('Year', flat=True).distinct().order_by('-Year')
    type_choices = Wines.objects.values_list('Type', flat=True).distinct().order_by('Type')
    country_choices = Wines.objects.values_list('Country', flat=True).distinct().order_by('Country')
    region_choices = Wines.objects.exclude(Region__isnull = True).exclude(Region__exact='').values_list('Region', flat=True).distinct().order_by('Region')
    grapes_choices = Wines.objects.exclude(Grapes__isnull=True).exclude(Grapes__exact='').values_list('Grapes', flat=True).distinct().order_by('Grapes')


    context = {
        'wines': wines,
        'search_query': search_query,
        'year_filter': year_filter,
        'type_filter': type_filter,
        'country_filter': country_filter,
        'region_filter': region_filter,
        'grapes_filter': grapes_filter,
        'sort_by': sort_by,
        'year_choices': year_choices,
        'type_choices': type_choices,
        'country_choices': country_choices,
        'region_choices': region_choices,
        'grapes_choices': grapes_choices,
    }
    return render(request, 'my_app/wine_list.html', context)

def spirit_list(request):
    spirits = Spirits.objects.all()
    search_query = request.GET.get('search', '')
    type_filter = request.GET.get('type', '')
    style_filter = request.GET.get('style', '')
    alcohol_filter = request.GET.get('alcohol', '')
    sort_by = request.GET.get('sort_by', '')

    if search_query:
        spirits = spirits.filter(Name__icontains=search_query)
    
    if type_filter:
        spirits = spirits.filter(Type__icontains=type_filter)
    
    if style_filter:
        spirits = spirits.filter(Style__icontains=style_filter)

    # Validate and filter alcohol_filter
    if alcohol_filter:
        try:
            alcohol_value = int(alcohol_filter)
            spirits = spirits.filter(AlcLvl=alcohol_value)
        except ValueError:
            pass  # Ignore invalid input

    if sort_by == 'price_asc':
        spirits = spirits.order_by('Price')
    elif sort_by == 'price_desc':
        spirits = spirits.order_by('-Price')
    
    type_choices = Spirits.objects.values_list('Type', flat=True).distinct().order_by('Type')
    style_choices = Spirits.objects.exclude(Style__isnull=True).exclude(Style__exact='').values_list('Style', flat=True).distinct().order_by('Style')
    alcohol_choices = Spirits.objects.exclude(AlcLvl__isnull=True).values_list('AlcLvl', flat=True).distinct().order_by('AlcLvl')

    context = {
        'spirits': spirits,
        'search_query': search_query,
        'sort_by': sort_by,
        'type_filter': type_filter,
        'type_choices': type_choices,
        'style_filter': style_filter,
        'style_choices': style_choices,
        'alcohol_filter': alcohol_filter,
        'alcohol_choices': alcohol_choices,
    }
    return render(request, 'my_app/spirit_list.html', context)

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