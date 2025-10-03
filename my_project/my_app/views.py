from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Wines, Cart, CartItem, Spirits, Order, OrderItem
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm, OrderForm, CustomSetPasswordForm
from django.contrib.auth import logout
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Count
from datetime import datetime, timedelta
from django.db.models import Sum
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetCompleteView
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.contrib.auth.decorators import user_passes_test
from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect


def index(request):
    return redirect('home')

def logout_view(request):
    next_url = request.GET.get('next', 'home')
    if next_url == '/home/cart/' or next_url == '/checkout/' or next_url == '/order_success/' or next_url == '/orders/' or next_url == '/home/statistics/' or next_url == '/admin_dashboard/' or next_url == '/profile':
        next_url = '/home/'
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
        return JsonResponse({'error': 'Not enough stock available.'}, status=400)

    # Get or create a cart for the user
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Get or create a cart item for the item
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        wine=item if item_type == 'wine' else None,
        spirit=item if item_type == 'spirit' else None,
        defaults={'price': item.Price}
    )

    if not created and cart_item.quantity + quantity > item.Qty:
        return JsonResponse({'error': 'Cannot add more items than available in stock. Check your cart.'}, status=400)

    
    if created:
        cart_item.quantity = quantity
    else:
        cart_item.quantity += quantity
    cart_item.save()

    # Return JSON response with updated cart item count
    cart_item_count = CartItem.objects.filter(cart__user=request.user).count()
    return JsonResponse({'cart_item_count': cart_item_count})

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

    year_choices = Wines.objects.exclude(Year__exact=0).values_list('Year', flat=True).distinct().order_by('-Year')
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
    
    # Check if social providers are configured
    can_google = False
    can_facebook = False
    try:
        from allauth.socialaccount.models import SocialApp
        can_google = SocialApp.objects.filter(provider='google').exists()
        can_facebook = SocialApp.objects.filter(provider='facebook').exists()
    except Exception:
        pass

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid input. Please try again.', extra_tags='signup-error')
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
        'next': next_url,
        'can_google': can_google,
        'can_facebook': can_facebook
    }
    return render(request, 'my_app/signup.html', context)

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_value = sum(item.price * item.quantity for item in cart_items)
    return render(request, 'my_app/cart.html', {'cart_items': cart_items, 'total_value': total_value})

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

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)
    total_value = sum(item.price * item.quantity for item in cart_items)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = total_value
            order.save()
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    wine=item.wine,
                    spirit=item.spirit,
                    quantity=item.quantity,
                    price=item.price,
                    name=item.wine.Name if item.wine else item.spirit.Name,
                    type=item.wine.Type if item.wine else item.spirit.Type,
                    year=item.wine.Year if item.wine else None,
                    grapes=item.wine.Grapes if item.wine else None,
                    country=item.wine.Country if item.wine else None,
                    region=item.wine.Region if item.wine else None,
                    alcohol_level=item.spirit.AlcLvl if item.spirit else None,
                    style=item.spirit.Style if item.spirit else None
                )
                if item.wine:
                    item.wine.Qty -= item.quantity
                    item.wine.save()
                elif item.spirit:
                    item.spirit.Qty -= item.quantity
                    item.spirit.save()
            cart_items.delete()
            return redirect('order_success')
    else:
        form = OrderForm()
    return render(request, 'my_app/checkout.html', {'form': form, 'cart_items': cart_items, 'total_value': total_value})

@login_required
def order_success(request):
    order = Order.objects.filter(user=request.user).latest('created_at')
    return render(request, 'my_app/order_succes.html', {'order': order})

@staff_member_required
def orders(request):
    orders = Order.objects.all()
    return render(request, 'my_app/orders.html', {'orders': orders})

@staff_member_required
def order_items(request, order_id):
    order = Order.objects.get(id=order_id)
    items = order.items.all()
    items_data = [
        {
            'name': item.name,
            'quantity': item.quantity,
            'price': item.price,
            'type': item.type,
            'year': item.year,
            'grapes': item.grapes,
            'country': item.country,
            'region': item.region,
            'alcohol_level': item.alcohol_level,
            'style': item.style
        } for item in items
    ]
    return JsonResponse({'items': items_data})

@staff_member_required
def mark_order_as_done(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = 'Done'
    order.save()
    return JsonResponse({'status': 'success'})

@staff_member_required
def mark_order_as_pending(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = 'Pending'
    order.save()
    return JsonResponse({'status': 'success'})

@staff_member_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return JsonResponse({'status': 'success'})

@staff_member_required
def statistics_view(request):
    last_month = datetime.today() - timedelta(days=30)
    most_sold_wines = OrderItem.objects.filter(order__created_at__gte=last_month, wine__Name__isnull=False).values('wine__Name').annotate(total_sold=Sum('quantity')).filter(total_sold__gt=0).order_by('-total_sold') 
    # filter used to show the wines that have been sold at least once, and we can change it to any value we want
    most_sold_spirits = OrderItem.objects.filter(order__created_at__gte=last_month, spirit__Name__isnull=False).values('spirit__Name').annotate(total_sold=Sum('quantity')).filter(total_sold__gt=0).order_by('-total_sold') 

    context = {
        'most_sold_wines': most_sold_wines,
        'most_sold_spirits': most_sold_spirits,
    }
    return render(request, 'my_app/statistics.html', context)

def terms(request):
    return render(request, 'my_app/terms-and-conditions.html')

def confidentialitypolicy(request):
    return render(request, 'my_app/confidentiality-policy.html')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'my_app/password_reset.html'
    email_template_name = 'my_app/password_reset_email.html'
    subject_template_name = 'my_app/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'my_app/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'my_app/password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'my_app/password_reset_complete.html'

# def wine_detail(request, wine_id):
#     wine = get_object_or_404(Wines, ID=wine_id)
#     return render(request, 'my_app/wine_detail.html', {'wine': wine})

# def spirit_detail(request, spirit_id):
#     spirit = get_object_or_404(Spirits, ID=spirit_id)
#     return render(request, 'my_app/spirit_detail.html', {'spirit': spirit})

@login_required
def profile_view(request):
    user = request.user
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    storage = get_messages(request)
    profile_messages = [message for message in storage if 'profile-' in message.tags]
    return render(request, 'my_app/profile.html', {'user': user, 'orders': orders, 'profile_messages': profile_messages})
    
@login_required
def profile_update(request):
    if request.method == 'POST':
        user = request.user
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        # Check if the username already exists
        if User.objects.filter(username=username).exclude(pk=user.pk).exists():
            messages.error(request, 'Username already exists.', extra_tags='profile-error')
            return redirect('profile_view')

        # Check if the email already exists
        if User.objects.filter(email=email).exclude(pk=user.pk).exists():
            messages.error(request, 'Email already exists.', extra_tags='profile-error')
            return redirect('profile_view')

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Invalid email format.', extra_tags='profile-error')
            return redirect('profile_view')

        # Update user information
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        messages.success(request, 'Profile updated successfully.', extra_tags='profile-success')
        return redirect('profile_view')

    return redirect('profile_view')

@login_required
def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    items = order.items.all()
    order_data = {
        'id': order.id,
        'created_at': order.created_at,
        'total_price': order.total_price,
        'status': order.status,
        'items': [
            {
                'product_name': item.wine.Name if item.wine else item.spirit.Name,
                'quantity': item.quantity,
                'price': item.price,
            } for item in items
        ]
    }
    return JsonResponse(order_data)

def cookie_policy(request):
    return render(request, 'my_app/cookies-policy.html')

@require_POST
@staff_member_required
def edit_wine(request, wine_id):
    if not request.user.is_staff:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)

    wine = get_object_or_404(Wines, ID=wine_id)
    data = json.loads(request.body)

    if data.get('action') == 'delete':
        wine.delete()
        return JsonResponse({'status': 'success', 'message': 'Wine deleted successfully'})
    
    wine.Name = data.get('name', wine.Name)
    wine.Price = data.get('price', wine.Price)
    wine.Qty = data.get('quantity', wine.Qty)
    wine.save()

    return JsonResponse({'status': 'success'})

@require_POST
@staff_member_required
def edit_spirit(request, spirit_id):
    if not request.user.is_staff:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)

    spirit = get_object_or_404(Spirits, ID=spirit_id)
    data = json.loads(request.body)

    if data.get('action') == 'delete':
        spirit.delete()
        return JsonResponse({'status': 'success', 'message': 'Spirit deleted successfully'})
    
    spirit.Name = data.get('name', spirit.Name)
    spirit.Price = data.get('price', spirit.Price)
    spirit.Qty = data.get('quantity', spirit.Qty)
    spirit.save()

    return JsonResponse({'status': 'success'})

def staff_or_group_required(group_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_staff or request.user.groups.filter(name=group_name).exists():
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("You do not have permission to access this page.")
        return _wrapped_view
    return decorator

@staff_or_group_required('Product Population')
def admin_dashboard(request):
    return render(request, 'my_app/admin_dashboard.html')
