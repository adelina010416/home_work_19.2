from django.shortcuts import render

from catalog.models import Product


# Create your views here.
def home(request):
    context = {
        'object_list': Product.objects.all()
    }
    return render(request, 'catalog/home.html', context)


def contacts(request):
    return render(request, 'catalog/contacts.html')


def product(request, pid):
    context = {
        'object': Product.objects.filter(id=pid)[0]
    }
    return render(request, 'catalog/product.html', context)
