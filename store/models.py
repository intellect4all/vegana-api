from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth import get_user_model



class Category(models.Model):
    name = models.CharField(max_length=50)
    class_icon = models.CharField(max_length=50, null=True, blank=True)
    slug = models.SlugField(editable=False)

    def save(self, *args, **kwargs):                                  # add this
        self.slug = slugify(self.name, allow_unicode=True)           # add this
        super().save(*args, **kwargs)   

    def __str__(self):
        return self.name
class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=150)
    actual_price = models.IntegerField()
    discount_price = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='tags', blank=True)
    slug = models.SlugField(unique=True, editable=False)
    description = models.TextField(max_length=3000, default="This is an auto generated product description.")
    featured_image = models.ImageField(null=True, blank=True)
    is_on_sale = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-created']

    #this returns the slug of the product
    def save(self, *args, **kwargs):                                  # add this
        self.slug = slugify(self.name, allow_unicode=True)            # add this
        super().save(*args, **kwargs)                                 # add this

    def get_absolute_url(self):
        return reverse('store:product', kwargs={'slug': self.slug})

    def get_price(self):
        if self.discount_price:
            return self.discount_price
        else:
            return self.actual_price
    

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.quantity} of {self.product.name}'

    def get_item_total_price(self):
        return self.quantity * self.product.get_price()    


class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    date_created = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_created']


class WishItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name

class Wishlist(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    items = models.ManyToManyField(WishItem)
    date_created = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_created']