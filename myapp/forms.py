from django import forms
from myapp.models import Order

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