from django.db import models
from io import BytesIO
from django.core.files import File
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.

class Usuario(models.Model):
    user = models.OneToOneField(User, null = True, on_delete = models.CASCADE)
    name = models.CharField(max_length=200, null = True)
    phone = models.CharField(max_length=200, null = True)
    email = models.CharField(max_length=200, null = True)
    profile_pic = models.ImageField(default = "usuario.png",null = True, blank = True)
    date_created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name

class Category(models.Model):
    title = models.CharField(max_length= 200, null = True)
    slug = models.SlugField(max_length=200, null = True) 
    ordering = models.IntegerField(default = 0)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('ordering',)

    def __str__(self):
        return self.title

class SubCategory(models.Model):
    title = models.CharField(max_length= 200, null = True)
    slug = models.SlugField(max_length=200, null = True) 
    category = models.ForeignKey(Category, null = True, on_delete = models.CASCADE)
    
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
    subcategory = models.ForeignKey(SubCategory, related_name='products', null = True, on_delete = models.CASCADE)
    brand = models.ForeignKey(Brand, related_name='products', null = True, on_delete = models.CASCADE)
    description = models.TextField(blank = True, null = True)
    price = models.FloatField(null = True)
    disccount = models.BooleanField(default = False)
    disccount_price = models.FloatField(blank = True, null = True)
    
    image = models.ImageField(upload_to = 'images/',blank = True, null = True)
    thumbnail = models.ImageField(upload_to = 'images/', blank = True, null = True) 
    date_added = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ('-date_added',)
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.thumbnail = self.make_thumbnail(self.image)

        super().save(*args, **kwargs)

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

class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.IntegerField(default = 1)


    def __str__(self):
        return self.product.name

class Order(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete = models.CASCADE, null = True)
    products = models.ManyToManyField(OrderProduct)
    start_date = models.DateTimeField(auto_now_add = True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default = False)

    