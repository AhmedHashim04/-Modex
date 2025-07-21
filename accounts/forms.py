from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext as _

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address', 'phone', 'governorate', 'alternate_phone']
        labels = {
            'address': _('Address'),
            'phone': _('Primary Phone'),
            'alternate_phone': _('Alternate Phone'),
            'governorate': _('Governorate'),
        }
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'alternate_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'governorate': forms.Select(attrs={'class': 'form-select'}),
        }

