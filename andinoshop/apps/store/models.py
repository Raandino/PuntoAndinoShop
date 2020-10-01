from django.db import models

# Create your models here.

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
    date_added = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ('-date_added',)
    def __str__(self):
        return self.name

