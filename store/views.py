
from django.contrib.auth import login
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render, get_list_or_404
# from django.template import context
from django.views.generic import View, DetailView
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *

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
            return redirect('store:cart')
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

@login_required
def checkout(request):
    all_categories = get_list_or_404(Category)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    billing_form = BillingAddForm()
    shipping_form = ShippingAddForm()
    detail_form = OrderDetailsForm()
    if order_qs.exists():
        order = order_qs[0]
        order_items = order.items.all()
        if order_items.exists():    
            cart_total = order.get_order_total()
            order_total = order.get_final_price()
            
            context = {
                'order_items': order_items,
                'all_categories': all_categories,
                'cart_total': cart_total,
                'order_total': order_total,
                'billing_form': billing_form,
                'shipping_form': shipping_form,
                'detail_form': detail_form,
                'order' : order
            }
            return render(request, 'store/checkout.html', context)
        else:
            messages.info(request, "You do not have any item in your cart, please continue shopping.")
            return redirect('store:home')
    else:
        messages.info(request, "You do not have an active order, please continue shopping.")
        return redirect('store:home')


class add_billing_address(View, LoginRequiredMixin):
    def post(self, *args, **kwargs):
        form = BillingAddForm(self.request.POST)
        print(form)
        if form.is_valid():
            print("cool")
            user = self.request.user
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            company = form.cleaned_data.get('company')
            address = form.cleaned_data.get('address')
            city = form.cleaned_data.get('city')
            post_code = form.cleaned_data.get('post_code')
            state =form.cleaned_data.get('state')
            phone = form.cleaned_data.get('phone')
            same_as_shipping = form.cleaned_data.get('same_as_shipping')
            billing_add = BillingAdd.objects.create(
                user=user, 
                first_name=first_name, 
                last_name=last_name, 
                company=company, 
                address=address, 
                city=city,
                post_code=post_code,
                state=state,
                phone=phone,
                same_as_shipping=same_as_shipping
                )
            billing_add.save()
            order_qs = Order.objects.filter(user=self.request.user, ordered=False)
            order = order_qs[0]
            order.billing = billing_add
            order.save()
            if billing_add.same_as_shipping:
                shipping_add = ShippingAdd.objects.create(
                user=user, 
                first_name=first_name, 
                last_name=last_name, 
                company=company, 
                address=address, 
                city=city,
                post_code=post_code,
                state=state,
                phone=phone,
                )
                shipping_add.save()
                order.shipping = shipping_add
                order.save()
                messages.info(self.request, "Billing Address successfully added and set as shipping address.")
                return redirect('store:checkout')
            messages.info(self.request, "Billing Address successfully added.")
            return redirect('store:checkout')
        else:
            messages.info(self.request, "Form not working")
            return redirect('store:home')

class add_shipping_address(View, LoginRequiredMixin):
    def post(self, *args, **kwargs):
        form = ShippingAddForm(self.request.POST)
        if form.is_valid():
            user = self.request.user
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            company = form.cleaned_data.get('company')
            address = form.cleaned_data.get('address')
            city = form.cleaned_data.get('city')
            post_code = form.cleaned_data.get('post_code')
            state =form.cleaned_data.get('state')
            phone = form.cleaned_data.get('phone')
            same_as_billing = form.cleaned_data.get('same_as_billing')
            shipping_add = ShippingAdd.objects.create(
                user=user, 
                first_name=first_name, 
                last_name=last_name, 
                company=company, 
                address=address, 
                city=city,
                post_code=post_code,
                state=state,
                phone=phone,
                same_as_billing=same_as_billing
                )
            shipping_add.save()
            order_qs = Order.objects.filter(user=self.request.user, ordered=False)
            shipping= ShippingAdd.objects.filter(
                user=user, 
                first_name=first_name, 
                last_name=last_name, 
                company=company, 
                address=address, 
                city=city,
                post_code=post_code,
                state=state,
                phone=phone,)[0]
            order = order_qs[0]
            order.shipping = shipping
            order.save()
            messages.info(self.request, "Shipping Address successfully added to the order.")
            return redirect('store:checkout')
        else:
            messages.info(self.request, "Form not working")
            return redirect('store:home')

class add_order_details(View, LoginRequiredMixin):
    def post(self, *args, **kwargs):
        form = OrderDetailsForm(self.request.POST)
        if form.is_valid():
            quote = form.cleaned_data.get('quote')
            user = self.request.user
            payment = form.cleaned_data.get('payment')
            agree = form.cleaned_data.get('agree')
            details = OrderDetail.objects.create(user=user, quote=quote, payment=payment, agree=agree)
            details.save()
            order_qs = Order.objects.filter(user=self.request.user, ordered=False)
            details= OrderDetail.objects.filter(
                user=user, quote=quote, payment=payment, agree=agree)[0]
            order = order_qs[0]
            order.details = details
            order.save()
            return redirect('store:checkout')
        else:
            messages.info(self.request, "Form not working")
            return redirect('store:home')

@login_required
def Cart(request):
    all_categories = Category.objects.all()
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        order_items = order.items.all()
        cart_total = order.get_order_total()
        context = {
            'order_items': order_items,
            'all_categories': all_categories,
            'cart_total': cart_total,
        }
        return render(request, 'store/cartlist.html', context)
    else:
        messages.info(request, "You do not have an active order")
        return redirect('store:home')

@login_required
def add_to_wishlist(request, slug):
    product = get_object_or_404(Product, slug=slug, is_on_sale=True)
    wish_item, created = WishItem.objects.get_or_create(user=request.user, product=product, ordered=False)
    wishlist_qs = Wishlist.objects.filter(user=request.user, ordered=False)
    if wishlist_qs.exists():
        wishlist = wishlist_qs[0]
        if wishlist.items.filter(product__slug=slug).exists():
            messages.info(request, f'{wish_item.product.name} already exists in your wishlist.')
            return redirect('store:home')
        else:
            wishlist.items.add(wish_item)
            messages.info(request, f'{wish_item.product.name} has been added to your wishlist.')
            return redirect('store:home')
    else:
        ordered_date = timezone.now()
        wishlist = Wishlist.objects.create(user=request.user, ordered_date=ordered_date)
        wishlist.items.add(wish_item)
        messages.info(request, f'{wish_item.product.name} has been added to your wishlist.')
        return redirect('store:home')

@login_required
def wishlist(request):
    all_categories = Category.objects.all()
    wishlist_qs = Wishlist.objects.filter(user=request.user, ordered=False)
    if wishlist_qs.exists():
        wishlist = wishlist_qs[0]
        wishlist_items = wishlist.items.all()
        context = {
            'wishlist': wishlist_items,
            'all_categories': all_categories,
        }
        return render(request, 'store/wishlist.html', context)
    else:
        messages.info(request, "You do not have a wishlist. Kindly add a product to your wishlist")
        return redirect('store:home')

@login_required
def add_wishlist_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug, is_on_sale=True)
    order_item, created = OrderItem.objects.get_or_create(user=request.user, product=product, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    wish_item, created = WishItem.objects.get_or_create(user=request.user, product=product, ordered=False)
    wishlist_qs = Wishlist.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__slug=product.slug).exists():
            order_item.quantity += 1
            order_item.save()
            wishlist = wishlist_qs[0]
            wishlist.items.remove(wish_item)
            msg = product.name + " already exists in your cart. The quantity has been incremented and removed from your wishlist."
            messages.info(request, msg)
            return redirect('store:wishlist')
        else:
            order.items.add(order_item)
            wishlist = wishlist_qs[0]
            wishlist.items.remove(wish_item)
            msg = product.name + " has been added to your cart and removed from your wishlist."
            messages.info(request, msg)
            return redirect('store:wishlist')
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        wishlist = wishlist_qs[0]
        wishlist.items.remove(wish_item)
        msg = product.name + " has been added to your cart and removed from your wishlist."
        messages.info(request, msg)
        return redirect('store:wishlist')

@login_required
def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_item = OrderItem.objects.get(user=request.user, product=product)
    order_qs= Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__slug=slug):
            order_item.delete()
            msg = product.name + " has been removed from your cart."
            messages.info(request, msg)
            return redirect('store:cart')
        else:
            msg = product.name + " is not in your cart."
            messages.info(request, msg)
            return redirect('store:cart')
    else:
        msg = "You do not have an active order, please continue shopping."
        messages.info(request, msg)
        return redirect('store:home')

@login_required
def remove_single_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_item = OrderItem.objects.get(user=request.user, product=product)
    order_qs= Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__slug=slug):
            order_item.quantity -= 1
            order_item.save()
            if order_item.quantity < 1 :
                order_item.delete()
                #order.items.remove(order_item)
            msg = "1 x of " + product.name + " has been removed from your cart."
            messages.info(request, msg)
            return redirect('store:cart')
        else:
            msg = product.name + " is not in your cart."
            messages.info(request, msg)
            return redirect('store:cart')
    else:
        msg = "You do not have an active order, please continue shopping."
        messages.info(request, msg)
        return redirect('store:home')

@login_required
def remove_from_wishlist(request, slug):
    product = get_object_or_404(Product, slug=slug)
    wishitem = WishItem.objects.get(user=request.user, product=product)
    wishlist_qs= Wishlist.objects.filter(user=request.user, ordered=False)
    if wishlist_qs.exists():
        wishlist = wishlist_qs[0]
        if wishlist.items.filter(product__slug=slug):
            wishlist.items.remove(wishitem)
            msg = product.name + " has been removed from your wishlist."
            messages.info(request, msg)
            return redirect('store:wishlist')
        else:
            msg = product.name + " is not in your wishlist."
            messages.info(request, msg)
            return redirect('store:wishlist')
    else:
        msg = "You have not added any item to your wishlist, please continue shopping."
        messages.info(request, msg)
        return redirect('store:home')

@login_required
def add_single_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug, is_on_sale=True)
    order_item, created = OrderItem.objects.get_or_create(
        user=request.user, product=product, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__slug=product.slug).exists():
            order_item.quantity += 1
            order_item.save()
            msg = "1 x " + product.name + " added."
            messages.info(request, msg)
            return redirect('store:cart')
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


# Checkout functionality views
@login_required
def add_single_to_checkout_cart(request, slug):
    product = get_object_or_404(Product, slug=slug, is_on_sale=True)
    order_item, created = OrderItem.objects.get_or_create(
        user=request.user, product=product, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__slug=product.slug).exists():
            order_item.quantity += 1
            order_item.save()
            msg = "1 x " + product.name + " added."
            messages.info(request, msg)
            return redirect('store:checkout')
        else:
            order.items.add(order_item)
            msg = product.name + " has been added to your cart."
            messages.info(request, msg)
            return redirect('store:checkout')
    else:
        msg = "You do not have an active order, please continue shopping."
        messages.info(request, msg)
        return redirect('store:home')


@login_required
def remove_single_from_checkout_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_item = OrderItem.objects.get(user=request.user, product=product)
    order_qs= Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__slug=slug):
            order_item.quantity -= 1
            order_item.save()
            if order_item.quantity < 1 :
                order_item.delete()
                # order.items.remove(order_item)
                # order_item.quantity = 1
                # order_item.save()
            msg = "1 x of " + product.name + " has been removed from your cart."
            messages.info(request, msg)
            return redirect('store:checkout')
        else:
            msg = product.name + " is not in your cart."
            messages.info(request, msg)
            return redirect('store:checkout')
    else:
        msg = "You do not have an active order, please continue shopping."
        messages.info(request, msg)
        return redirect('store:home')


@login_required
def remove_from_checkout_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_item = OrderItem.objects.get(user=request.user, product=product)
    order_qs= Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__slug=slug):
            order_item.delete()
            msg = product.name + " has been removed from your cart."
            messages.info(request, msg)
            return redirect('store:checkout')
        else:
            msg = product.name + " is not in your cart."
            messages.info(request, msg)
            return redirect('store:checkout')
    else:
        msg = "You do not have an active order, please continue shopping."
        messages.info(request, msg)
        return redirect('store:home')

class payment(View, LoginRequiredMixin):
    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        pass