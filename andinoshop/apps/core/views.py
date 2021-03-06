import random
from django.shortcuts import render,  redirect
from apps.store.decorators import allowed_users, admin_only
from django.db import connection

from apps.store.models import Product, Category
# Create your views here.

@admin_only
def frontpage(request):
    #pagina principal
    products = list(Product.objects.filter(disccount = True, alta = False))
    print(connection.queries)
    featured = list(Product.objects.filter(is_featured = True, alta = False))
    new = list(Product.objects.filter(alta = False).order_by('-date_added')[:10])
    if len(featured) >= 3:
        featured = random.sample(featured, 3)

    if len(products) >= 3:
        products = random.sample(products, 3)

    if len(new) >= 3:
        new = random.sample(new, 3)
    context = {
        'products': products,
        'featured': featured,
        'new': new,
    }

    return render(request, 'frontpage.html', context)
