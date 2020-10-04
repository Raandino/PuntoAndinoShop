from django.shortcuts import render,  redirect
from apps.store.decorators import allowed_users, admin_only

from apps.store.models import Product, Category
# Create your views here.


def frontpage(request):
    products = Product.objects.filter(disccount = True)

    context = {
        'products': products
    }
    return render(request, 'frontpage.html', context)
