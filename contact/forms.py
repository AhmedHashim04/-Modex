from django import forms
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class EmailForm(forms.Form):
    name = forms.CharField(
        max_length=25,
        label=_("Name"),
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z]+(?:\s+[a-zA-Z]+)*$",
                message=_("Name should only contain letters and spaces"),
            )
        ],
    )

    from_email = forms.EmailField(
        label=_("Email"),
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,63}$",
                message=_("Invalid email address"),
            )
        ]
    )

    title = forms.CharField(
        required=True,
        label=_("Subject"),
        widget=forms.Textarea(attrs={
            "rows": 1,
            "placeholder": _("Subject")
        }),
    )

    message = forms.CharField(
        required=True,
        label=_("Message"),
        widget=forms.Textarea(attrs={
            "rows": 5,
            "placeholder": _("Your message")
        }),
    )
