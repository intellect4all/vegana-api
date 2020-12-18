from django.contrib import admin
from .models import *

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    '''Admin View for Product'''

    list_display = ('name', 'actual_price', 'is_on_sale', 'created', 'slug')
    list_filter = ('created', 'is_on_sale', 'category', 'tags')
    
    search_fields = ('name',)
    

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    '''Admin View for Category'''

    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    '''Admin View for Tag'''

    list_display = ('name',)
    search_fields = ('name',)
    verbose_name = 'Tag'
    verbose_name_plural = 'Tags'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    '''Admin View for OrderItem'''
    list_display = ('user', 'ordered', 'product', 'quantity')
    list_filter = ('ordered',)
    search_fields = ('user',)
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    '''Admin View for Order'''
    list_display = ('user', 'ordered', 'ordered_date', 'ref')
    list_filter = ('ordered',  'date_created', 'ordered_date')
    search_fields = ('user', 'ref')
    readonly_fields = ('ref', 'user', 'ordered_date', 'items', )
    

@admin.register(Wishlist)
class WishListAdmin(admin.ModelAdmin):
    '''Admin View for WishList'''

    list_display = ('user', 'ordered')
    list_filter = ('ordered', 'date_created')
    search_fields = ('user',)

@admin.register(WishItem)
class WishItemAdmin(admin.ModelAdmin):
    '''Admin View for WishItem'''
    list_display = ('user', 'ordered', 'product',)
    list_filter = ('ordered',)
    search_fields = ('user',)


@admin.register(BillingAdd)
class BillingAddAdmin(admin.ModelAdmin):
    '''Admin View for BillingAdd'''

    list_display = ('user', 'last_name', 'first_name', 'address', 'city', 'state', 'phone', 'same_as_shipping', )
    list_filter = ('same_as_shipping', 'state',)
    
    # readonly_fields = ('user', 'last_name', 'first_name', 'address', 'city', 'state', 'phone', 'same_as_shipping', )
    search_fields = ('user', 'last_name', 'first_name', 'address', 'city', 'state', 'phone', 'same_as_shipping', )
    ordering = ('-id',)

@admin.register(ShippingAdd)
class ShippingAddAdmin(admin.ModelAdmin):
    '''Admin View for ShippingAdd'''

    list_display = ('user', 'last_name', 'first_name', 'address', 'city', 'state', 'phone', 'same_as_billing', )
    list_filter = ('same_as_billing', 'state',)
    
    # readonly_fields = ('user', 'last_name', 'first_name', 'address', 'city', 'state', 'phone', 'same_as_billing', )
    search_fields = ('user', 'last_name', 'first_name', 'address', 'city', 'state', 'phone', 'same_as_billing', )
    ordering = ('-id',)

@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    '''Admin View for OrderDetail'''

    list_display = ('user', 'quote', 'payment', 'agree' )
    list_filter = ('payment', 'agree',)
    search_fields = ('quote',)
    ordering = ('-id',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    '''Admin View for Customer'''

    list_display = ('user', 'state', 'city', 'phone', 'address')
    list_filter = ('state', 'city')
    search_fields = ('state', 'city', 'user', 'phone', 'address')
    ordering = ('-id',)