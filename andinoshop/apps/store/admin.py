from django.contrib import admin
from .models import Category, Product, Brand, ProductImage, Usuario, OrderProduct, Order, ProductReview, likedProduct
# Register your models here.

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Usuario)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(ProductReview)
admin.site.register(likedProduct)