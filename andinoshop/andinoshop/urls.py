"""andinoshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from apps.core.views import frontpage
from apps.store.views import *


urlpatterns = [
    path('', frontpage, name='frontpage'),
    path('search/', search, name='search'),
    path('update-address/<str:pk>/', update_address, name = 'update-address'),
    path('admin/', admin.site.urls),
    path('register/', registerPage, name = 'registerPage'),
    path('login/', loginPage, name = 'loginPage'),
    path('logout/', logoutUser, name = 'logout'),
    path('featured/', featured, name='featured'),
    path('novedades/', new, name='new'),
    path('coins/', coins_view, name = 'coins'),
    path('discount/', discount, name='discount'),
    path('cart/', CartView.as_view(), name = 'cart'),
    path('profile/', profilePage, name = 'profilePage'),
    path('add-to-cart/<slug>/', add_to_cart, name = 'add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name = 'remove_from_cart'),
    path('remove-quantity-cart/<slug>/', remove_quantity_from_cart, name = 'remove_quantity_from_cart'),
    path('like-products/<slug>/', likeproducts, name = 'like-products'),
    path('remove-from-list/<slug>/', remove_from_favorites, name='remove-from-list'),
    path('save-for-later/<slug>/', save_for_later, name = 'save-for-later'),
    path('move-to-cart/<slug>/', move_to_cart, name = 'move-to-cart'),
    path('checkout-address/', select_shipping, name = 'shipping'),
    path('comparación/<slug>/', compare_similar, name = 'compare-similar'),
    path('remove-from-later/<slug>/', remove_from_later, name='remove-from-later'),
    path('<slug:category_slug>/<slug:slug>/', product_detail, name='product_detail'),
    path('favorites/', likedproductsview, name = 'favorites'),
    path('address/', address_view, name = 'address-view'),
    path('create-address/', address_create, name = 'address_create'),
    path('shipping/<str:pk>', shipping, name = 'selected-address'),
    path('payment/', payment_view, name = 'payment'),
    path('<slug:slug>/', category_detail, name='category_detail'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
