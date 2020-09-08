from django.shortcuts import render

# Create your views here.
def shop(request):
    context = {}
    return render(request, 'shop/index.html', context)