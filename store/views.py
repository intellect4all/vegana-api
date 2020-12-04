from django.shortcuts import render
from django.views.generic import View, DetailView
from .models import *

# Create your views here.

def Home(request):
    context = {
        'name': 'Odewole'
    }
    return render(request, 'store/index.html', context)


def Product(request, slug):
    
    context = {

    }
    return render(request, 'store/product-details.html', context)
