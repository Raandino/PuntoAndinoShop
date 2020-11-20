from django.db import models
from io import BytesIO
from django.core.files import File
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.conf import settings
from PIL import Image
from taggit.managers import TaggableManager
# Create your models here.

class Usuario(models.Model):
    user = models.OneToOneField(User, null = True, on_delete = models.CASCADE)
    name = models.CharField(max_length=200, null = True)
    phone = models.CharField(max_length=200, null = True)
    email = models.CharField(max_length=200, null = True)
    profile_pic = models.ImageField(default = "usuario.png",null = True, blank = True)
    date_created = models.DateTimeField(auto_now_add = True)
    coins = models.IntegerField(default = 0)

    def __str__(self):
        return self.name

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null = True)
    full_name = models.CharField(max_length=300)
    address_1 = models.CharField(max_length=350)
    address_2 = models.CharField(max_length=350, null = True)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=8)

    def __str__(self):
        return self.address_1
    

class Category(models.Model):
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank = True, null = True)
    title = models.CharField(max_length= 200, null = True)
    slug = models.SlugField(max_length=200, null = True) 
    ordering = models.IntegerField(default = 0)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('ordering',)

    def __str__(self):
        return self.title


class Brand(models.Model):
    name = models.CharField(max_length=200, null = True)
    slug = models.SlugField(max_length=200, null = True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length = 255, null = True)
    slug = models.SlugField(max_length=200)
    category = models.ForeignKey(Category, related_name='products', on_delete = models.CASCADE)
    brand = models.ForeignKey(Brand, null = True, on_delete = models.CASCADE)
    description = models.TextField(blank = True, null = True)
    original_price = models.FloatField(blank=True, null=True)
    price = models.FloatField(null = True, blank=True, default=0)
    is_featured = models.BooleanField(default = False)
    is_new = models.BooleanField(default = False)
    disccount = models.BooleanField(default = False)
    dis = models.IntegerField(blank=True, default = 0)
    quantity_available = models.IntegerField(default = 1)
    tags = TaggableManager()

    
    image = models.ImageField(upload_to = 'images/',blank = True, null = True)
    thumbnail = models.ImageField(upload_to = 'images/', blank = True, null = True) 
    date_added = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.thumbnail = self.make_thumbnail(self.image)
        if not self.pk:
            self.price = self.original_price

        if self.disccount:
            div = (100-self.dis)/100
            self.price = div * self.price

        
        else: 
            self.price = self.original_price

        
        super().save(*args, **kwargs)
        
        
    def get_dis(self):
        save = self.original_price-self.price
        return save
     
    def get_absolute_url(self):
        return '/%s/%s/' % (self.category.slug, self.slug)

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)
        
        thumb_io = BytesIO()
        img.save(thumb_io, 'PNG', quality = 85)

        thumbnail = File(thumb_io, name = image.name)

        return thumbnail

    def get_rating(self):
        total = sum(int(review['stars']) for review in self.reviews.values())

        if self.reviews.count() > 0:
            return total / self.reviews.count()
        else: 
            return 0   

    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart(self):
        return reverse("remove-from-cart", kwargs={
            'slug': self.slug
        })

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name = 'images', on_delete = models.CASCADE)
    image = models.ImageField(upload_to = 'static/images/',blank = True, null = True)
    thumbnail = models.ImageField(upload_to = 'static/images/', blank = True, null = True)

    def save(self, *args, **kwargs):
        self.thumbnail = self.make_thumbnail(self.image)

        super().save(*args, **kwargs)

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)
        
        thumb_io = BytesIO()
        img.save(thumb_io, 'PNG', quality = 85)

        thumbnail = File(thumb_io, name = image.name)

        return thumbnail 

    def __str__(self):
        return self.product.name
        
class ProductReview(models.Model):
    product = models.ForeignKey(Product, related_name = 'reviews', on_delete = models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'reviews', on_delete = models.CASCADE)

    content = models.TextField()
    stars = models.IntegerField()

    date_added = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.product.name
    


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, null = True, blank = True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.user.username


class Order(models.Model):
    STATUS = (
        ('Pendiente', 'Pendiente'),
        ('En Camino', 'En Camino'),
        ('Entregado', 'Entregado'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null = True)
    start_date = models.DateTimeField(auto_now_add = True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default = False)
    status = models.CharField(max_length=200, null = True, choices = STATUS, default='Pendiente')
    shipping_address = models.ForeignKey(Address, related_name='shipping_address', on_delete=models.SET_NULL, blank = True, null = True)
    payment = models.ForeignKey(Payment, related_name='payment', on_delete=models.SET_NULL, blank = True, null = True)


    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_product in self.products.all():
            total += order_product.get_total_product_price()
        return total
    def total_envio(self):
        total = 0
        for order_product in self.products.all():
            total += order_product.get_total_product_price()
        if total > 0:
            return total+30


class OrderProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null = True)
    ordered =  models.BooleanField(default = False)
    order = models.ForeignKey(Order, related_name='products', on_delete = models.CASCADE, null = True)
    product = models.ForeignKey(Product, related_name='products', on_delete = models.DO_NOTHING)
    price = models.FloatField()
    quantity = models.IntegerField(default = 1)
    save_later = models.BooleanField(default = False)


    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def save(self, *args, **kwargs):
        self.price = self.quantity * self.product.price
        super().save(*args, **kwargs)    

    def get_total_product_price(self):
        return self.quantity * self.product.price

    def get_amount_save(self):
        return self.quantity * self.product.get_dis()


class Listaliked(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null = True)
    name = models.CharField(max_length = 255)

    def __str__(self):
        return self.name


class likedProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null = True)
    product = models.ForeignKey(Product, related_name='productos', on_delete = models.CASCADE)
    lista = models.ForeignKey(Listaliked, related_name='lista', on_delete = models.CASCADE)

    def __str__(self):
        return f"{self.product.name} in {self.lista.name} from {self.lista.user}"

