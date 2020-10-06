from .models import Category
from django.contrib.auth import authenticate, login, logout

def menu_categories(request):
    categories = Category.objects.filter(parent = None)

    return{'menu_categories': categories}

