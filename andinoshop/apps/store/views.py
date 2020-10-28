import random
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm, CustomerForm
from .models import Product, Category, OrderProduct, Order, Usuario, ProductReview, Brand
from .decorators import unauthenticated_user
from django.contrib.auth.models import Group
from django.core.paginator import Paginator, EmptyPage
from django.contrib import messages
from django.views.generic import ListView
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django.views.generic import View


# Create your views here.
#BUSQUEDA DE PRODUCTOS DIRECTA
def search(request):
    query = request.GET.get('query')
    products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains = query))

    p = Paginator(products, 16)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)

    context = {
        'query': query,
        'products': page_obj
    }

    return render(request, 'search.html', context)


#DETALLES DEL PRODUCTO EN SI
def product_detail(request, slug, category_slug):
    product = get_object_or_404(Product, slug=slug)
    usuario = Usuario.objects.all()
    related_products = list(product.category.products.filter(parent=None).exclude(id=product.id))
    if len(related_products) >= 3:
        related_products = random.sample(related_products, 3)

        
    if request.method == 'POST' and request.user.is_authenticated:
        stars = request.POST.get('stars', 3)
        content = request.POST.get('content', '')
        review = ProductReview.objects.create(product=product, user=request.user, stars=stars, content=content)
        
        return redirect('product_detail', category_slug=category_slug, slug=slug)

    imagesstring = "{'thumbnail': '%s', 'image': '%s'}," % (product.thumbnail.url, product.image.url)

    for image in product.images.all():
        imagesstring = imagesstring + ("{'thumbnail': '%s', 'image': '%s'}," % (image.thumbnail.url, image.image.url))
    context = {
        'product': product,
        'imagesstring': imagesstring,
        'related_products': related_products,
        'usuario': usuario,
    }

    print(connection.queries)

    return render(request, 'product_detail.html', context)


#QUERY PARA EL FILTRO
def is_valid_queryparam(param):
    return param != '' and param is not None



#PRODUCTOS DE LA CATEGORIA SELECCIONADA
def category_detail(request, slug):

    products = Product.objects.all()
    category = get_object_or_404(Category, slug=slug)
    pricemin = request.GET.get('price_min')
    pricemax = request.GET.get('price_max')  
    featured = request.GET.get('featured')
    discount = request.GET.get('discount')
    review = request.GET.get('review')
    sorting = request.GET.get('sorting')
    new = request.GET.get('new')
    marca = request.GET.get('test')
    marca_vals = set(request.GET.getlist('test'))


    products = products.filter(Q(category__parent=category)|Q(category=category))
    q = products.order_by('brand').distinct('brand')

    if is_valid_queryparam(pricemin):
        products = products.filter(price__gte=pricemin)

    if is_valid_queryparam(pricemax):
        products = products.filter(price__lt=pricemax)

    if marca :
        products = products.filter(brand__name__in=request.GET.getlist('test'))


    if featured == 'on':
        products = products.filter(is_featured=True)

    if discount == 'on':
        products = products.filter(disccount=True)

    if new == 'on':
        products = products.filter(is_new=True)


    if is_valid_queryparam(review) and review != 'Estrellas':
        products = products.filter(reviews__stars=review).distinct()

    if is_valid_queryparam(sorting):
        products = products.order_by(sorting)

    
    p = Paginator(products, 9)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except EmptyPage:
        page_obj = p.get_page(1)
    
    context = {
        'category': category,
        'products' : products,
        'q': q,
        'pricemin': pricemin,
        'pricemax': pricemax,
        'sorting': sorting,
        'featured': featured,
        'discount': discount,
        'new': new,
        'review': review,
        'marca': marca,
        'marca_vals': marca_vals,

    }
    print(connection.queries)

    return render(request, 'category_detail.html', context)



#MUESTRA LOS PRODUCTOS DESTACADOS
def featured(request):
    products = Product.objects.filter(is_featured=True)
    p = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    context = {
        'products': page_obj,
    }

    return render(request, 'featured_products.html', context)


#MUESTRA LAS NOVEDADES
def new(request):
    products = Product.objects.filter(is_new=True)
    p = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    context = {
        'products': page_obj,
    }

    return render(request, 'novedades.html', context)
    

#MUESTRA LOS PRODUCTOS EN DESCUENTO
def discount(request):
    products = Product.objects.filter(disccount=True)
    p = Paginator(products, 16)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    context = {
        'products': page_obj,
    }

    return render(request, 'discount_page.html', context)


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

#MUESTRA EL PERFIL DEL USUARIO
def profilePage(request):
    usuario = request.user.usuario
    form = CustomerForm(instance = usuario)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance = usuario)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'customer.html', context)



#PAGINA DEL CARRITO

class CartView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            print(connection.queries)
            return render(self.request, 'cart.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "No tienes productos en el carrito")
            return redirect("/")






#FUNCIONALIDAD PARA AÑADIR AL CARRO
@login_required(login_url = 'loginPage')
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug = slug)
    order_product, created = OrderProduct.objects.get_or_create(
        product = product,
        user = request.user,
        ordered = False
    )
    order_qs = Order.objects.filter(user = request.user, ordered = False) 
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product_id = product.id).exists():
            order_product.quantity += 1
            order_product.save()
        else:
            order.products.add(order_product)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user = request.user, ordered_date = ordered_date)
        order.products.add(order_product)
    return redirect('cart')


