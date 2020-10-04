from django.contrib import admin
from .models import Category, Product, SubCategory, Brand, ProductImage, Usuario, OrderProduct, Order
# Register your models here.

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Usuario)
admin.site.register(Order)
admin.site.register(OrderProduct)