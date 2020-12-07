from typing import Tuple
from django.shortcuts import get_object_or_404, redirect, render
from django.template import context
from django.views.generic import View, DetailView
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

# Create your views here.

def HomePage(request):
    all_categories = Category.objects.all()
    trending_products = Product.objects.filter(is_on_sale=True)
    best_selling_products = Product.objects.filter(is_on_sale=True)
    new_products = Product.objects.filter(is_on_sale=True)
    context = {
        'trending_products': trending_products,
        'best_selling_products': best_selling_products,
        'new_products': new_products,
        'all_categories' : all_categories,
    }
    return render(request, 'store/index.html', context)


def ProductDetails(request, slug):
    all_categories = Category.objects.all()
    product = get_object_or_404(Product, slug=slug, is_on_sale=True)
    new_arrivals = Product.objects.filter(is_on_sale=True)[:3]
    context = {
       'new_arrivals' : new_arrivals,
       'product' : product,
       'all_categories' : all_categories,
    }
    return render(request, 'store/product-details.html', context)

       
def CategoryView(request, category):
    all_categories = Category.objects.all()
    cat_products = Product.objects.filter(category__name=category.title(), is_on_sale=True)
    if cat_products.exists():
        context = {
            'cat_products': cat_products,
            'all_categories' : all_categories,
        }
        return render(request, 'store/shop.html', context)
    else:
        messages.info(request, "The category is empty or does not exist")
        return redirect('store:home')