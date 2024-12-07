"""
URL configuration for my_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.admin.views.decorators import staff_member_required
from my_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', views.logout_view, name='logout_view'),
    path('home/', views.home, name='home'),
    path('home/contact/', views.contact, name='contact'),
    path('home/product_list/', views.product_list, name='product_list'),
    path('product_list/wines/', views.wine_list, name='wine_list'),
    path('product_list/spirits/', views.spirit_list, name='spirit_list'),
    path('add_to_cart/<str:item_type>/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('home/cart/', views.cart_view, name='cart_view'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_success/', views.order_success, name='order_success'),
    path('orders/', views.orders, name='orders'),
    path('orders/<int:order_id>/items/', views.order_items, name='order_items'),
    # other URL patterns
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
