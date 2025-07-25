from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Review


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        (5, "★★★★★"),
        (4, "★★★★"),
        (3, "★★★"),
        (2, "★★"),
        (1, "★"),
    ]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.Select,
        label=_("Rating"),
    )

    content = forms.CharField(
        widget=forms.Textarea(attrs={
            "rows": 4,
            "placeholder": _("Write your review here...")
        }),
        label=_("Review"),
        required=True,
        max_length=1000,
    )

    class Meta:
        model = Review
        fields = ["content", "rating"]

    def clean_content(self):
        content = self.cleaned_data.get("content", "").strip()
        if not content:
            raise forms.ValidationError(_("Review content cannot be empty."))
        return content
