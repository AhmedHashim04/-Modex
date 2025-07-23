from django import forms

from .models import Address, Order


class OrderCreateForm(forms.ModelForm):
    address = forms.ModelChoiceField(
        queryset=Address.objects.none(), label="Shipping Address", empty_label=None)

    class Meta:
        model = Order
        fields = ["address", "payment_method", "shipping_method"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["address"].queryset = Address.objects.filter(user=user)


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'full_name', 'phone', 'governorate', 'city', 'address_line', 'is_default', 'notes'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'governorate': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City/Center'}),
            'address_line': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Detailed Address', 'rows': 2}),
            'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Additional Notes (optional)', 'rows': 1}),
        }
        labels = {
            'full_name': 'Full Name',
            'phone': 'Phone Number',
            'governorate': 'Governorate',
            'city': 'City/Center',
            'address_line': 'Detailed Address',
            'is_default': 'Set as default address',
            'notes': 'Additional Notes',
        }