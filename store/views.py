
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
# from django.template import context
# from django.views.generic import View, DetailView
from .models import *
# from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

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
        'all_categories': all_categories,
    }
    return render(request, 'store/index.html', context)


def ProductDetails(request, slug):
    all_categories = Category.objects.all()
    product = get_object_or_404(Product, slug=slug, is_on_sale=True)
    new_arrivals = Product.objects.filter(is_on_sale=True)[:3]
    context = {
        'new_arrivals': new_arrivals,
        'product': product,
        'all_categories': all_categories,
    }
    return render(request, 'store/product-details.html', context)


def CategoryView(request, category):
    all_categories = Category.objects.all()
    cat_products = Product.objects.filter(
        category__name=category.title(), is_on_sale=True)
    if cat_products.exists():
        context = {
            'cat_products': cat_products,
            'all_categories': all_categories,
        }
        return render(request, 'store/shop.html', context)
    else:
        messages.info(request, "The category is empty or does not exist")
        return redirect('store:home')

@login_required
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug, is_on_sale=True)
    order_item, created = OrderItem.objects.get_or_create(
        user=request.user, product=product, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__slug=product.slug).exists():
            order_item.quantity += 1
            order_item.save()
            msg = product.name + " already exists in your cart. The quantity has been incremented."
            messages.info(request, msg)
            return redirect('store:product', slug=slug)
        else:
            order.items.add(order_item)
            msg = product.name + " has been added to your cart."
            messages.info(request, msg)
            return redirect('store:home')
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        msg = product.name + " has been added to your cart."
        messages.info(request, msg)
        return redirect('store:home')


def Cart(request):
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        order_items = order.items.all()
        context = {
            'order_items': order_items,
        }
        return render(request, 'store/cartlist.html', context)
    else:
        messages.info(request, "You do not have an active order")
        return redirect('store:home')


def add_to_wishlist(request, slug):
    product = get_object_or_404(Product, slug=slug, is_on_sale=True)
    order_item, created = OrderItem.objects.get_or_create(user=request.user, product=product, ordered=False)
    wishlist_qs = Wishlist.objects.filter(user=request.user, ordered=False)
    if wishlist_qs.exists():
        wishlist = wishlist_qs[0]
        if wishlist.items.filter(product__slug=slug).exists:
            messages.info(request, f'{order_item.product.name} already exists in your wishlist.')
            return redirect('store:home')
        else:
            wishlist.items.add(order_item)
            messages.info(request, f'{order_item.product.name} has been added to your wishlist.')
            return redirect('store:home')
    else:
        ordered_date = timezone.now()
        wishlist = Wishlist.objects.create(user=request.user, ordered_date=ordered_date)
        wishlist.items.add(order_item)
        messages.info(request, f'{order_item.product.name} has been added to your wishlist.')
        return redirect('store:home')
        
def wishlist(request):
    wishlist_qs = Wishlist.objects.filter(user=request.user, ordered=False)
    if wishlist_qs.exists():
        wishlist = wishlist_qs[0]
        wishlist_items = wishlist.items.all()
        context = {
            'wishlist': wishlist_items,
        }
        return render(request, 'store/wishlist.html', context)
    else:
        messages.info(request, "You do not have a wishlist. Kindly add a product to your wishlist")
        return redirect('store:home')