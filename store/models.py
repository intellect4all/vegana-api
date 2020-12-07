from django.db import models
from django.utils.text import slugify
from django.urls import reverse



class Category(models.Model):
    name = models.CharField(max_length=50)
    class_icon = models.CharField(max_length=50, null=True, blank=True)
    slug = models.SlugField()

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
    description = models.TextField(max_length=3000)
    featured_image = models.ImageField(null=True, blank=True)
    is_on_sale = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-created']

    #this returns the slug of the product
    def save(self, *args, **kwargs):                                  # add this
        self.slug = slugify(self.name, allow_unicode=True)           # add this
        super().save(*args, **kwargs)                                 # add this

    def get_absolute_url(self):
        return reverse('store:product', kwargs={'slug': self.slug})



# Create your models here.
