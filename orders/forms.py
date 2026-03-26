"""
Order Checkout Form
"""
from django import forms


class CheckoutForm(forms.Form):
    """Form for collecting delivery details at checkout"""
    address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter your full delivery address'}),
        max_length=500
    )
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'placeholder': '+91 9876543210'})
    )
    payment_method = forms.ChoiceField(
        choices=[('cod', 'Cash on Delivery')],
        widget=forms.RadioSelect,
        initial='cod'
    )
