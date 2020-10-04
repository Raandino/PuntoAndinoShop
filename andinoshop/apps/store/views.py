from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm, CustomerForm
from .models import Product, Category, OrderProduct, Order, Usuario
from .decorators import unauthenticated_user
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def search(request):
    query = request.GET.get('query')
    products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains = query))

    context = {
        'query': query,
        'products': products
    }

    return render(request, 'search.html', context)

def product_detail(request, slug, category_slug):
    product = get_object_or_404(Product, slug=slug)

    imagesstring = "{'thumbnail': '%s', 'image': '%s'}," % (product.thumbnail.url, product.image.url)

    for image in product.images.all():
        imagesstring = imagesstring + ("{'thumbnail': '%s', 'image': '%s'}," % (image.thumbnail.url, image.image.url))
    context = {
        'product': product,
        'imagesstring': imagesstring
    }

    return render(request, 'product_detail.html', context)

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.all()
    context = {
        'category': category,
        'products' : products
    }

    return render(request, 'category_detail.html', context)

#def add_to_cart(request, slug):
#   product = get_object_or_404(Product, slug = slug)
#    order_product = OrderProduct.objects.create(product = product)
@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            first_name = form.cleaned_data.get('first_name')
            group = Group.objects.get(name = 'customer')
            user.groups.add(group)
            Usuario.objects.create(
                user = user,
                name = user.first_name + ' ' +user.last_name,
                email = user.email,
            )
            messages.success(request, 'Cuenta creada satisfactoriamente '+first_name)
            return redirect('loginPage')

    context = {'form': form}
    return render(request, 'register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('frontpage')

        else:
            messages.info(request, 'Datos Invalidos')


    context = {}
    return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('frontpage')


def profilePage(request):
    usuario = request.user.usuario
    form = CustomerForm(instance = usuario)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance = usuario)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'customer.html', context)

@login_required(login_url = 'loginPage')
def cart(request):
    return render(request, 'cart.html')

def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug = slug)
    order_product = OrderProduct.objects.create(product = product)
    order_qs = Order.objects.filter(usuario = request.usuario, ordered = False) 
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product_slug = product.slug).exists():
            order_product.quantity += 1
            order_product.save()
    
    else:
        order = Order.objects.create(usuario = request.usuario)
        order.products.add(order_product)
    return redirect('cart')