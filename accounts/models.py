from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

from django.core.validators import RegexValidator

class Profile(models.Model):
    EGYPT_GOVERNORATES = [
        ('C', _('Cairo')),
        ('GZ', _('Giza')),
        ('ALX', _('Alexandria')),
        ('ASN', _('Aswan')),
        ('AST', _('Assiut')),
        ('BNS', _('Beni Suef')),
        ('BH', _('Beheira')),
        ('IS', _('Ismailia')),
        ('MN', _('Minya')),
        ('MNF', _('Monufia')),
        ('MT', _('Matrouh')),
        ('KFS', _('Kafr El Sheikh')),
        ('DK', _('Dakahlia')),
        ('SHG', _('Sohag')),
        ('SHR', _('Sharqia')),
        ('PTS', _('Port Said')),
        ('DT', _('Damietta')),
        ('FYM', _('Fayoum')),
        ('GH', _('Gharbia')),
        ('KB', _('Qalyubia')),
        ('LX', _('Luxor')),
        ('WAD', _('New Valley')),
        ('SUZ', _('Suez')),
        ('SIN', _('North Sinai')),
        ('SIS', _('South Sinai')),
        ('QH', _('Qena')),
        ('RSH', _('Red Sea')),
    ]

    egyptian_phone_validator = RegexValidator(
        regex=r'^(01[0125])[0-9]{8}$',
        message=_("Phone number must start with 010, 011, 012, or 015 and be 11 digits.")
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(
        max_length=11,
        validators=[egyptian_phone_validator],
        verbose_name=_("Primary Phone Number"),
        help_text=_("Please enter an Egyptian phone number starting with 010, 011, 012, or 015.")
    )
    alternate_phone = models.CharField(
        max_length=11,
        blank=True,
        null=True,
        validators=[egyptian_phone_validator],
        verbose_name=_("Alternate Phone Number (optional)"),
        help_text=_("You can enter another Egyptian phone number for contact (optional).")
    )
    address = models.TextField(
        blank=True,
        verbose_name=_("Detailed Address"),
        help_text=_("Please write your address in detail, e.g., district, building number, apartment number, street name, and any additional details to facilitate order delivery.")
    )
    governorate = models.CharField(
        max_length=10,
        choices=EGYPT_GOVERNORATES,
        blank=True,
        verbose_name=_("Governorate")
    )
    wishlist = models.ManyToManyField('product.Product', blank=True, related_name='wishlists')

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self):
        return self.user.username
