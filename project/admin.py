# myproject/admin.py
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.apps import apps

class MyAdminSite(AdminSite):
    site_header = 'لوحة التحكم بمتجر محمد توفيق'
    site_title = 'لوحة التحكم بمتجر محمد توفيق'
    index_title = 'مرحبًا بك في لوحة الإدارة'

    def get_app_list(self, request):
        app_order = [
            'product',
            'order',
            'features',
            'accounts',
            'cart',
            'home',
            'contact',
        ]

        app_dict = self._build_app_dict(request)

        ordered_apps = []

        for app_label in app_order:
            if app_label in app_dict:
                ordered_apps.append(app_dict[app_label])

        for app_label in app_dict:
            if app_label not in app_order:
                ordered_apps.append(app_dict[app_label])

        return ordered_apps



# سجل موقعك المخصص
custom_admin_site = MyAdminSite(name='myadmin')
