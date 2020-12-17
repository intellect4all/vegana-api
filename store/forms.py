from django import forms 
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

    # quote = forms.CharField(max_length=1000, required=False)
    # payment =  forms.ModelChoiceField()
    # agree = forms.BooleanField(default=False)