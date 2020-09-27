from django.db import models

# Create your models here.

class Client(models.Model):
    name = models.CharField(max_length=200, null = True)
    phone = models.CharField(max_length=200, null = True)
    email = models.CharField(max_length=200, null = True)
    password = models.CharField(max_length=200, null = True)
    date_created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name

class Type_User(models.Model):
    name = models.CharField(max_length=200, null = True)

    def __str__(self):
        return self.name

class User(models.Model):
    name = models.CharField(max_length=200, null = True)
    phone = models.CharField(max_length=200, null = True)
    email = models.CharField(max_length=200, null = True)
    username = models.CharField(max_length=200, null = True)
    password = models.CharField(max_length=200, null = True)
    type_user = models.ForeignKey(Type_User, null = True, on_delete = models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name

class Measure(models.Model):
    measure = models.CharField(max_length=100, null = True)

    def __str__(self):
        return self.measure


class Category(models.Model):
    name = models.CharField(max_length=200, null = True)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=200, null = True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, null = True)
    brand = models.ForeignKey(Brand, null = True, on_delete = models.SET_NULL) 
    description = models.CharField(max_length=300, null = True)
    tax_apply = models.BooleanField(null = True)
    category = models.ForeignKey(Category, null = True, on_delete = models.SET_NULL)

    def __str__(self):
        return self.name

class Inventory(models.Model):
    product = models.ForeignKey(Product, null = True, on_delete = models.SET_NULL)
    user = models.ForeignKey(User, null = True, on_delete = models.SET_NULL)
    quantity = models.IntegerField(null = True)
    measure = models.ForeignKey(Measure, null = True, on_delete = models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add = True)
    date_modify = models.DateTimeField(auto_now_add = True)
    price = models.FloatField(null = True)
    
    def __str__(self):
        return self.product.name


class Address(models.Model):
    client = models.ForeignKey(Client, null = True, on_delete = models.SET_NULL)
    addres_1 = models.CharField(max_length=300, null = True)
    addres_2 = models.CharField(max_length=300, null = True)
    city = models.CharField(max_length = 250, null = True)
    status = models.BooleanField(null = True)

    def __str__(self):
        return self.client.name

class Status(models.Model):
    name = models.CharField(max_length = 200, null = True)

    def __str__(self):
        return self.name

class Order(models.Model):
    order_code = models.AutoField(primary_key = True)
    prefix = models.CharField(max_length=20, default = 'ORDNI')
    date_order = models.DateTimeField(auto_now_add = True)
    date_delivered = models.DateTimeField(auto_now_add = True)
    client = models.ForeignKey(Client, null = True, on_delete = models.SET_NULL)
    address = models.ForeignKey(Address, null = True, on_delete = models.SET_NULL)
    subtotal = models.FloatField(null = True)
    tax_total = models.FloatField(null = True)
    delivery = models.FloatField(null = True)
    status = models.ForeignKey(Status, null = True, on_delete = models.SET_NULL)
    total = models.FloatField(null = True)

    @property
    def order_id(self):
        return f"{self.prefix}{self.order_code}"

class Order_Detail(models.Model):
    order = models.ForeignKey(Order, null = True, on_delete = models.SET_NULL)
    product = models.ForeignKey(Product, null = True, on_delete = models.SET_NULL)
    quantity = models.IntegerField(null = True)
    price = models.FloatField(null = True)
    tax = models.FloatField(null = True)
    subtotal = models.FloatField(null = True)

    def __str__(self):
        return self.product

class Tax_Rate(models.Model):
    value = models.FloatField(null = True)
    date_modify = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.value