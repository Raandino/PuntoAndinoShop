import random, datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required
from apps.store.decorators import allowed_users, admin_only
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm, CustomerForm, AddressForm, CouponForm, OrderForm, ProductForm
from .models import Product, Category, OrderProduct, Order, Usuario, ProductReview, Brand, likedProduct, Listaliked, Address, Payment, Coupon
from .decorators import unauthenticated_user
from django.contrib.auth.models import Group
from django.template.loader import get_template
from django.core.paginator import Paginator, EmptyPage
from django.contrib import messages
from django.views.generic import ListView
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django.views.generic import View
from taggit.managers import TaggableManager
from io import BytesIO
from django.http import HttpResponse
from xhtml2pdf import pisa


import stripe
stripe.api_key = "sk_test_51HpNstHKhVhWsHEkwcl8cL6uizY5xfJR2KMx5F25ddUlKvFAID87RzJ1mZfHgxmz0FbUAm09eHm29PqJyOdMroZv00oBQOhCVz"

# `source` is obtained with Stripe.js; see https://stripe.com/docs/payments/accept-a-payment-charges#web-create-token


# Create your views here.
#BUSQUEDA DE PRODUCTOS DIRECTA
def search(request):
    query = request.GET.get('query')
    products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains = query)).filter(alta = False)

    p = Paginator(products, 50)
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
    product.num_visits = product.num_visits + 1
    product.save()
    if product.num_visits > 15:
        product.is_featured = True
        product.save()
    usuario = Usuario.objects.all()
    related_products = list(product.category.products.all().exclude(id=product.id))
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

    products = Product.objects.filter(alta = False)
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
        'products' : page_obj,
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
    products = Product.objects.filter(is_featured=True, alta = False)
    p = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    context = {
        'products': page_obj,
    }

    return render(request, 'featured_products.html', context)


#MUESTRA LAS NOVEDADES
def new(request):
    products = Product.objects.filter(alta = False).order_by('-date_added')[:10]
    p = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    context = {
        'products': page_obj,
    }

    return render(request, 'novedades.html', context)
    

#MUESTRA LOS PRODUCTOS EN DESCUENTO
def discount(request):
    products = Product.objects.filter(disccount=True, alta = False)
    p = Paginator(products, 12)
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
            messages.success(request, 'Información actualizada')
    context = {'form': form}
    return render(request, 'customer.html', context)



#PAGINA DEL CARRITO

class CartView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            pro = OrderProduct.objects.filter(order = order.pk, save_later = False)
            save = OrderProduct.objects.filter(user = self.request.user, save_later = True)
            later = OrderProduct.objects.filter(user = self.request.user, save_later = True)
            test = False

            order_products = OrderProduct.objects.filter(user = self.request.user, ordered = False, save_later = False)
            for product in order_products:
                if product.product.quantity_available < 1:
                    test = True
            context = {
                'object': order,
                'pro': pro,
                'save': save,
                'later': later,
                'test': test,

            }
            return render(self.request, 'cart.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "No tienes productos en el carrito")
            return redirect("/")






#FUNCIONALIDAD PARA AÑADIR AL CARRO
@login_required(login_url = 'loginPage')
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug = slug)
    order_qs = Order.objects.filter(user = request.user, ordered = False) 
    if order_qs.exists():
        order = order_qs[0]
        order_productos = OrderProduct.objects.filter(order = order.pk)
        pro = OrderProduct.objects.filter(user = request.user, save_later = True)
        if pro.filter(product__slug = product.slug).exists():
            messages.info(request, "Producto en la lista de guardados para más tarde.")
            return redirect('cart')
        else:
            if order_productos.filter(product__slug = product.slug).exists():
                order_product = order_productos.get(product__slug = product.slug)
                order_product.quantity += 1
                if order_product.quantity > order_product.product.quantity_available:
                    messages.info(request, "No esta disponible esa cantidad del producto")
                else:
                    order_product.save()
                    messages.info(request, "La cantidad del producto fue actualizada.")
            else:
                order_product = OrderProduct.objects.create(product=product, user=request.user, ordered=False, order = order )
                messages.info(request, "El producto fue agregado a su carrito.")
                return redirect('cart')
            
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user = request.user, ordered_date = ordered_date)
        order_product = OrderProduct.objects.create(product=product, user=request.user, ordered=False, order = order )
        messages.info(request, "El producto fue agregado a su carrito.")
    return redirect('cart')

def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug = slug)
    order_qs = Order.objects.filter(user = request.user, ordered = False) 
    order = order_qs[0]
    order_productos = OrderProduct.objects.filter(order = order.pk)
    order_product = order_productos.get(product__slug = product.slug)
    order_product.delete()
    messages.info(request, "El producto fue eliminado de tu carrito.")

    return redirect('cart')


def remove_quantity_from_cart(request, slug):
    product = get_object_or_404(Product, slug = slug)
    order_qs = Order.objects.filter(user = request.user, ordered = False) 
    order = order_qs[0]
    order_productos = OrderProduct.objects.filter(order = order.pk)
    order_product = order_productos.get(product__slug = product.slug)
    if order_product.quantity > 1:
        order_product.quantity -= 1
        order_product.save()
        messages.info(request, "La cantidad del producto fue actualizada de tu carrito.")
    else:
        order_product.delete()
        messages.info(request, "El producto fue eliminado de tu carrito.")

    return redirect('cart')





def save_for_later(request, slug):
    product = get_object_or_404(Product, slug = slug)
    order_qs = Order.objects.filter(user = request.user, ordered = False) 
    order = order_qs[0]
    order_productos = OrderProduct.objects.filter(order = order.pk, save_later = False)
    producto = order_productos.filter(product__slug = product.slug)
    producto.update(save_later = True, quantity = 0, order = None)
    messages.info(request, "Producto guardado para más tarde.")
    return redirect('cart')

def remove_from_later(request, slug):
    product = get_object_or_404(Product, slug = slug)
    order_product = OrderProduct.objects.get(user = request.user, product__slug = product.slug, save_later = True)
    order_product.delete()
    messages.info(request, "Producto eliminado de su lista de guardados para más tarde.")
    return redirect('cart')


def move_to_cart(request, slug):
    product = get_object_or_404(Product, slug = slug)
    order_qs = Order.objects.filter(user = request.user, ordered = False) 
    order = order_qs[0]
    order_productos = OrderProduct.objects.filter(user = request.user, save_later = True)
    producto = order_productos.filter(product__slug = product.slug)
    producto.update(save_later = False, quantity = 1, order = order.pk)
    messages.info(request, "Producto movido al carrito.")
    return redirect('cart')

def compare_similar(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = product.tags.similar_objects() 
    if len(related_products) >= 3:
        related_products = random.sample(related_products, 3)

    context = {
        'related_products': related_products,
        'product': product,
    }
    return render(request, 'compare.html', context)

    

@login_required(login_url = 'loginPage')
def address_view(request):
    address = Address.objects.filter(user = request.user)
    context = {
        'address': address,
    }
    return render(request,'address.html', context)
@login_required(login_url = 'loginPage')
def address_create(request):
    if request.method == 'POST':
        fullname = request.POST.get('full_name')
        address_1 = request.POST.get('address_1')
        address_2 = request.POST.get('address_2')
        city = request.POST.get('city')
        phone = request.POST.get('phone')

        address = Address.objects.create(user = request.user, full_name = fullname, address_1 = address_1, address_2 = address_2, city = city, phone = phone)
        messages.info(request, "Direccion añadida")
        return redirect('address-view')
    return render(request, 'create_address.html')


@login_required(login_url = 'loginPage')
def update_address(request, pk):
    address = Address.objects.get(id = pk)
    form = AddressForm(instance = address)

    if request.method == 'POST':
        form = AddressForm(request.POST, instance = address)
        if form.is_valid():
            form.save()
            messages.info(request, "Dirección actualizada")
            return redirect('address-view')
    context = {
        'form': form,
    }
    return render(request,'update_address.html', context)

def delete_address(request, pk):
    address = Address.objects.get(user = request.user, id = pk)
    address.delete()
    messages.success(request, 'Dirección eliminada satisfactoriamente')
    return redirect('address-view')

@login_required(login_url = 'loginPage')
def select_shipping(request):
    address = Address.objects.filter(user = request.user)
    if request.method == 'POST':
        fullname = request.POST.get('full_name')
        address_1 = request.POST.get('address_1')
        address_2 = request.POST.get('address_2')
        city = request.POST.get('city')
        phone = request.POST.get('phone')

        address = Address.objects.create(user = request.user, full_name = fullname, address_1 = address_1, address_2 = address_2, city = city, phone = phone)
        messages.info(request, "Direccion añadida")
        return redirect('shipping')
    context = {
        'address' : address
    }
    return render(request, 'select_address.html', context)

def shipping(request, pk):
    address = Address.objects.get(id = pk)
    order = Order.objects.get(user=request.user, ordered=False)
    order.shipping_address = address
    order.save()
    return redirect('payment')

def payment_view(request):
    order = Order.objects.get(user = request.user, ordered = False)
    if request.method == 'POST':
        order = Order.objects.get(user = request.user, ordered = False)
        token = request.POST.get('stripeToken')
        amount = int(order.total_envio() * 100)

        try:
            charge = stripe.Charge.create(
                amount = amount,
                currency="nio",
                source= token,
            )

            
                    #Creando el pago para tener un registro
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = request.user
            payment.amount = order.total_envio()
            payment.save()

            #reduciendo cantidad del producto del inventario
            cant = OrderProduct.objects.filter(user = request.user, ordered = False, save_later = False)
            for t in cant:
                q = t.product.quantity_available
                s = t.quantity
                x = q-s
                t.product.quantity_available = x
                t.product.save()
                t.original_price = t.product.price
                t.save()


            #Asignando el pago a la orden
            order_products = order.products.all()
            order_products.update(ordered=True)
            for product in order_products:
                product.save()





            if len(order_products) > 3:
                coins = 10
                usuario = request.user.usuario
                coins_user = usuario.coins
                total = coins + coins_user
                usuario.coins = total
                usuario.save()


            order.ordered = True
            order.payment = payment
            order.total = order.total_envio()
            order.ordered_date = timezone.now()
            order.save()

            messages.success(request, "Tu orden se ha realizado correctamente!")
            return redirect("orders")
        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get('error', {})
            messages.warning(request, f"{err.get('message')}")
            return redirect("/")
        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.warning(request, "Demasiadas peticiones enviadas")
            return redirect("/")
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.warning(request, "Parametros incorrectos")
            return redirect("/")
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.warning(request, "Fallo en la autenticación")
            return redirect("/")
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.warning(request, "Error en la conexión")
            return redirect("/")
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.warning(request, "Algo salio mal, no fue cobrado, intente nuevamente!")
            return redirect("payment")
        except Exception as e:
            # send email to ourselves
            messages.warning(request, "Error")
            return redirect("/")
    context = {
        'order': order,
        'couponform': CouponForm,
    }
    return render(request, 'payment.html', context)




def coins_view(request):
    usuario = request.user.usuario
    coins = usuario.coins
    context = {
        'coins': coins,
    }
    return render(request, 'coins.html', context)

def is_valid_queryparam(param):
    return param != '' and param is not None

def orders_client(request):
    order = Order.objects.filter(user = request.user, ordered = True)
    order_product = OrderProduct.objects.filter(order = order)
    status = request.GET.get('status')
    sorting = request.GET.get('sorting')


    if is_valid_queryparam(sorting) and sorting != 'Escoge...':
        order = order.order_by(sorting)
    
    if status:
        order = order.filter(status__in = request.GET.getlist('status'))

    p = Paginator(order, 8)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except EmptyPage:
        page_obj = p.get_page(1)

    context = {
        'order': page_obj,
        'order_product': order_product,
        'sorting': sorting,
        'status': status,
    }
    return render(request, 'orders.html', context )

def order_detail(request, pk):
    order = Order.objects.get(user = request.user, id = pk)
    context = {
        'order': order,
    }
    return render(request, 'order_detail.html', context)

def change_address(request, pk):
    order = Order.objects.get(user = request.user, id = pk)
    address = Address.objects.filter(user = request.user)
    if request.method == 'POST':
        fullname = request.POST.get('full_name')
        address_1 = request.POST.get('address_1')
        address_2 = request.POST.get('address_2')
        city = request.POST.get('city')
        phone = request.POST.get('phone')

        address = Address.objects.create(user = request.user, full_name = fullname, address_1 = address_1, address_2 = address_2, city = city, phone = phone)
        messages.info(request, "Direccion añadida")
        return redirect('change-address', order.id)
    context = {
        'order': order,
        'address': address,
    }

    return render(request, 'change_address.html', context)

def change_address_confirm(request, pk, order_pk):
    address = Address.objects.get(id = pk)
    order = Order.objects.get(user=request.user, id = order_pk)
    order.shipping_address = address
    order.save()
    messages.info(request, "Dirección cambiada")
    return redirect('order-detail', order.id)

def render_to_pdf(template_src, context_dict = {}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

    if not pdf.err:
        return result.getvalue()
    
    return None

def invoice_download(request, pk):
    order = Order.objects.get( id = pk)
    pdf = render_to_pdf('order_pdf.html', {'order': order})

    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        content = "attachment; filename=Factura #%s.pdf" %  pk
        response['Content-Disposition'] = content

        return response
    
    return HttpResponse("No se encontro")

def test(request, pk):
    order = Order.objects.get(user = request.user , id = pk)
    context = {
        'order': order,
    }
    return render (request, 'order_pdf.html', context)


def get_coupon(request, code):
    try: 
        coupon = Coupon.objects.get(code = code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "Este cupon no existe")
        return redirect('payment')

def add_coupon(request):
    if request.method == 'POST':
        form = CouponForm(request.POST or None)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            order = Order.objects.get(user = request.user, ordered = False) 
            coupon = get_coupon(request, code)
            order.coupon = coupon
            order.save()
            messages.success(request, "Cupon agregado")
            return redirect('payment')
    return None

def buy_coupon(request, number):
    coupon = Coupon.objects.get(porcentage = number)
    if coupon.porcentage == 10:
        usuario = request.user.usuario
        if usuario.coins >= 50:
            usuario.coins -= 50
            usuario.save()
            context = {
                'codigo': coupon,
            }
            messages.success(request, 'Cupon canjeado exitosamente!')
            return render(request, 'coupon-charge.html', context)
        else:
            messages.warning(request, "No tienes monedas suficientes")
            return redirect('coins')
    elif coupon.porcentage == 22:
        usuario = request.user.usuario
        if usuario.coins >= 120:
            usuario.coins -= 120
            usuario.save()
            context = {
                'codigo': coupon,
            }
            messages.success(request, 'Cupon canjeado exitosamente!')
            return render(request, 'coupon-charge.html', context)
        else:
            messages.warning(request, "No tienes monedas suficientes")
            return redirect('coins')
    elif coupon.porcentage == 30:
        usuario = request.user.usuario
        if usuario.coins >= 250:
            usuario.coins -= 250
            usuario.save()
            context = {
                'codigo': coupon,
            }
            messages.success(request, 'Cupon canjeado exitosamente!')
            return render(request, 'coupon-charge.html', context)
        else:
            messages.warning(request, "No tienes monedas suficientes")
            return redirect('coins')


def orders_admin(request):
    order = Order.objects.filter( ordered = True)
    order_product = OrderProduct.objects.filter(order = order)
    status = request.GET.get('status')
    sorting = request.GET.get('sorting')
    user = request.GET.get('user')
    date_min = request.GET.get('from')
    date_max = request.GET.get('to')
    
    if is_valid_queryparam(user):
        order = order.filter(user__usuario__name__icontains=user)

    if is_valid_queryparam(sorting) and sorting != 'Escoge...':
        order = order.order_by(sorting)
    
    if status:
        order = order.filter(status__in = request.GET.getlist('status'))

    if is_valid_queryparam(date_min):
        order = order.filter(ordered_date__gte = date_min)

    if is_valid_queryparam(date_max):
        order = order.filter(ordered_date__lt = date_max)

    p = Paginator(order, 12)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except EmptyPage:
        page_obj = p.get_page(1)
    context = {
        'order': page_obj,
        'order_product': order_product,
        'sorting': sorting,
        'status': status,
        'user': user,
    }
    return render(request, 'order_admin.html', context)

def order_detail_admin(request, pk):
    order = Order.objects.get(id = pk)
    form = OrderForm(instance = order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance = order)
        if form.is_valid():
            form.save()
            messages.info(request, "Estado de orden actualizado")
            return redirect('order-detail-admin', order.id)
    context = {
        'order': order,
        'form': form,
    }
    return render(request, 'order_detail_admin.html', context)


def admin_front(request):
    orders = Order.objects.filter(ordered = True)
    total_orders = orders.count()
    delivered = orders.filter(status = 'Entregado').count()
    order = orders.filter().order_by('-id')[:5]
    pending = orders.filter(status = 'Pendiente').count()


    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    pending_today = orders.filter(status = 'Pendiente', ordered_date__range=(today_min, today_max))
    q = 0
    for p in pending_today:
        q += p.total

    context = {
        'orders': orders,
        'order': order,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending,
        'pending_today': pending_today,
        'q': q,
    }
    return render(request, 'front_admin.html', context)

def admin_products(request):
    products = Product.objects.all()
    categories = Category.objects.filter(parent = None)
    product = request.GET.get('product')
    categorias = request.GET.get('categorias')

    if is_valid_queryparam(product):
        products = products.filter(name__icontains = product)
    
    if is_valid_queryparam(categorias) and categorias != 'Escoger Categoria...':
        products = products.filter(Q(category__parent=categorias)|Q(category=categorias))

    p = Paginator(products, 12)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except EmptyPage:
        page_obj = p.get_page(1)
    context = {
        'products': page_obj,
        'categories': categories,
    }

    return render(request, 'products_admin.html', context)

def create_product(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto agregado!")
            return redirect('admin-products')

    context = {
        'form': form,
    }
    return render(request, 'create_product.html', context)

@login_required(login_url = 'loginPage')
def likeproducts(request, slug):
    product = get_object_or_404(Product, slug = slug)
    liked = likedProduct.objects.filter(user = request.user)
    if liked.filter(product =  product).exists():
        messages.info(request, "Ya tienes agregado este producto en tu lista.")
        return redirect('favorites')
    else:
        product_like = likedProduct.objects.create(user = request.user, product = product)
        messages.info(request, "Producto agregado a su lista de favoritos.")
        return redirect('favorites')
        

@login_required(login_url = 'loginPage')
def likedproductsview(request):
    liked = likedProduct.objects.filter(user = request.user)
    lista = Listaliked.objects.filter(user = request.user)
    context =  {
        'liked': liked,
        'lista': lista,
    }
    return render(request,'favorites.html', context )

def create_lista(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        lista = Listaliked.objects.create(user = request.user, name = name)
        messages.info(request, "Lista creada")
        return redirect('favorites')
    return render(request, 'create_lista.html')

def view_lista(request, pk):
    lista = Listaliked.objects.get(user = request.user ,id = pk)
    liked = likedProduct.objects.filter(user = request.user, lista = lista)

    context = {
        'lista': lista,
        'liked': liked,
    }

    return render(request, 'lista_view.html', context)


@login_required(login_url = 'loginPage')
def add_to_favorite(request, slug):
    product = Product.objects.get(slug = slug)
    listas = Listaliked.objects.filter(user = request.user)
    if request.method == 'POST':
        name = request.POST.get('name')
        lista = Listaliked.objects.create(user = request.user, name = name)
        messages.info(request, "Lista creada")
        return redirect('add-favorite', product.slug)

    context = {
        'product': product,
        'listas': listas,
    }
    return render(request, 'add_favorites.html', context)

def add_favorite_confirm(request, slug, pk):
    product = Product.objects.get(slug = slug)
    lista = Listaliked.objects.get(user = request.user, id = pk)
    lista_products = likedProduct.objects.filter(lista = lista.pk)
    if lista_products.filter(product  = product ).exists():
        messages.info(request, "Este producto ya esta en su lista")
        return redirect('view-lista', lista.id)
    else:
        lista_product = likedProduct.objects.create(user = request.user, product = product, lista = lista)
        lista_product.save()
        messages.info(request, "Producto Agregado a la lista!")
        return redirect('view-lista', lista.id)

def delete_lista(request, pk):
    lista = Listaliked.objects.get(user = request.user, id = pk)
    lista.delete()
    messages.success(request, 'Lista eliminada satisfactoriamente')
    return redirect('favorites')

def update_product(request, pk):
    product = Product.objects.get(id = pk)
    form = ProductForm(instance = product)

    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES, instance = product)
        if form.is_valid():
            form.save()
            messages.info(request, "Producto actualizado")
            return redirect('admin-products')
    context = {
        'form': form,
    }
    return render(request,'edit_product.html', context)

def categories_admin(request):
    categories = Category.objects.filter(parent = None)
    context = {
        'category': categories,
    }
    return render(request, 'categories_admin.html', context)