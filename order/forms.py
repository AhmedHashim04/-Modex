from django import forms

from .models import Address, Order,ShippingOption


class OrderCreateForm(forms.ModelForm):
    address = forms.ModelChoiceField(
        queryset=Address.objects.all(), label="Shipping Address", empty_label=None
    )

    shipping_option = forms.ModelChoiceField(
        queryset=ShippingOption.objects.none(),
        widget=forms.RadioSelect,
        required=True,
        label="Shipping Option"
    )

    class Meta:
        model = Order
        fields = ['full_name', 'phone', 'notes', 'address', 'payment_method', 'shipping_method', 'shipping_option']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'you can write notes here like 123-street or any address details', 'rows': 1}),
        }
        labels = {
            'full_name': 'Full Name',
            'phone': 'Phone Number',
            'notes': 'Additional Notes',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["address"].queryset = Address.objects.filter(user=user)
            default_address = user.addresses.filter(is_default=True).first()
            if default_address:
                self.fields["shipping_option"].queryset = ShippingOption.objects.all()

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
             'governorate', 'city', 'address_line', 'is_default'
        ]
        widgets = {
            'governorate': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City/Center'}),
            'address_line': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Detailed Address', 'rows': 2}),
            'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'governorate': 'Governorate',
            'city': 'City/Center',
            'address_line': 'Detailed Address',
            'is_default': 'Set as default address',
        }