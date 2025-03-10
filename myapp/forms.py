from django import forms
from myapp.models import Order
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client', 'product', 'num_units']
        widgets = {
            'client': forms.RadioSelect(),
        }
        labels = {
            'num_units': 'Quantity',
            'client': 'Client Name',
        }


class InterestForm(forms.Form):
    INTEREST_CHOICES = [
        (1, 'Yes'),
        (0, 'No')
    ]

    interested = forms.ChoiceField(
        choices=INTEREST_CHOICES,
        widget=forms.RadioSelect(),
    )

    quantity = forms.IntegerField(
        min_value=1,
        initial=1
    )

    comments = forms.CharField(
        widget=forms.Textarea,
        label='Additional Comments',
        required=False
    )

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), min_length=8)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not re.search(r'\d', password):
            raise ValidationError("Password must contain at least one digit.")
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Password must contain at least one uppercase letter.")
        return password