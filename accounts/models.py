from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    EGYPT_GOVERNORATES = [
        ('C', 'القاهرة'),
        ('GZ', 'الجيزة'),
        ('ALX', 'الإسكندرية'),
        ('ASN', 'أسوان'),
        ('AST', 'أسيوط'),
        ('BNS', 'بني سويف'),
        ('BH', 'البحيرة'),
        ('IS', 'الإسماعيلية'),
        ('MN', 'المنيا'),
        ('MNF', 'المنوفية'),
        ('MNFY', 'المنوفية'),
        ('MT', 'مطروح'),
        ('KFS', 'كفر الشيخ'),
        ('DK', 'الدقهلية'),
        ('SHG', 'سوهاج'),
        ('SHR', 'الشرقية'),
        ('PTS', 'بورسعيد'),
        ('DT', 'دمياط'),
        ('FYM', 'الفيوم'),
        ('GH', 'الغربية'),
        ('KB', 'القليوبية'),
        ('LX', 'الأقصر'),
        ('WAD', 'الوادي الجديد'),
        ('SUZ', 'السويس'),
        ('SIN', 'شمال سيناء'),
        ('SIS', 'جنوب سيناء'),
        ('QH', 'قنا'),
        ('RSH', 'البحر الأحمر'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    governorate = models.CharField(
        max_length=10,
        choices=EGYPT_GOVERNORATES,
        blank=True,
        verbose_name="المحافظة"
    )

    def __str__(self):
        return self.user.username
