from django import forms
from django.db.models.fields import TextField
from django.forms.widgets import TextInput 
from .models import *

class BillingAddForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    company = forms.CharField(max_length=50)
    address = forms.CharField(max_length=500)
    city = forms.CharField(max_length=50)
    post_code = forms.CharField(max_length=50)
    state = forms.CharField(max_length=50)
    phone = forms.CharField(max_length=12)
    same_as_shipping = forms.BooleanField(required=False)

class ShippingAddForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    company = forms.CharField(max_length=50)
    address = forms.CharField(max_length=500)
    city = forms.CharField(max_length=50)
    post_code = forms.CharField(max_length=50)
    state = forms.CharField(max_length=50)
    phone = forms.CharField(max_length=12)
    same_as_billing = forms.BooleanField(required=False)


class OrderDetailsForm(forms.ModelForm):
    class Meta:
        model = OrderDetail
        fields = '__all__'
        exclude = ['user']
        widgets = {'payment': forms.RadioSelect}

class CustomerInfoForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user', 'billing', 'shipping', 'joined']
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'phone': TextInput(attrs={'class': 'form-control'}),
            'address': TextInput(attrs={'class': 'form-control'}),
            'city': TextInput(attrs={'class': 'form-control'}),
            'state': TextInput(attrs={'class': 'form-control'}),
            'post_code': TextInput(attrs={'class': 'form-control'}),
            'country': TextInput(attrs={'class': 'form-control'}),
            'birthday': TextInput(attrs={'class': 'form-control'}),
            
        
        }