from django.shortcuts import render

from apps.store.models import Product, Category
# Create your views here.

def frontpage(request):
    products = Product.objects.filter(disccount = True)

    context = {
        'products': products
    }
    return render(request, 'frontpage.html', context)

