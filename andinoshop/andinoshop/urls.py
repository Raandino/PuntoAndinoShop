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
from apps.store.views import product_detail,featured, category_detail, search, registerPage, loginPage, logoutUser, profilePage, cart, add_to_cart, discount, new


urlpatterns = [
    path('', frontpage, name='frontpage'),
    path('search/', search, name='search'),
    path('admin/', admin.site.urls),
    path('register/', registerPage, name = 'registerPage'),
    path('login/', loginPage, name = 'loginPage'),
    path('logout/', logoutUser, name = 'logout'),
    path('featured/', featured, name='featured'),
    path('novedades/', new, name='new'),
    path('discount/', discount, name='discount'),
    path('cart/', cart, name = 'cart'),
    path('profile/', profilePage, name = 'profilePage'),
    path('add-to-cart/<slug>/', add_to_cart, name = 'add-to-cart'),
    path('<slug:category_slug>/<slug:slug>/', product_detail, name='product_detail'),
    path('<slug:slug>/', category_detail, name='category_detail'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
