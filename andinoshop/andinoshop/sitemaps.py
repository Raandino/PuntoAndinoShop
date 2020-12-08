from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

from apps.store.models import Category, Product

class StaticViewSitemap(Sitemap):
    def items(self):
        return ['frontpage']

    def location(self, item):
        return reverse(item)

class CategorySiteMap(Sitemap):
    def items(self):
        return Category.objects.all()

class ProductSiteMap(Sitemap):
    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.date_added