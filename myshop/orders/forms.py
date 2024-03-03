from django import forms
from localflavor.us.forms import USZipCodeField
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        postal_code = USZipCodeField()
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city',]