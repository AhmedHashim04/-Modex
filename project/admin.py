# myproject/admin.py
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.apps import apps
from django.contrib import messages
from django.core.cache import cache
from django.urls import path
from django.shortcuts import redirect

class MyAdminSite(AdminSite):
    site_header = 'لوحة التحكم بمتجر محمد توفيق'
    site_title = 'لوحة التحكم بمتجر محمد توفيق'
    index_title = 'مرحبًا بك في لوحة الإدارة'

    def get_app_list(self, request):
        app_order = [
            'product',
            'order',
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


    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('clear-cache/', self.admin_view(self.clear_cache_view), name='clear-cache'),
        ]
        return custom_urls + urls

    def clear_cache_view(self, request):
        cache.clear()
        messages.add_message(request, messages.SUCCESS, "✅ تم مسح الكاش بنجاح.")
        return redirect('myadmin:index')

    def index(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['show_clear_cache'] = True
        return super().index(request, extra_context=extra_context)

# instance
admin_site = MyAdminSite(name='myadmin')


# سجل موقعك المخصص
custom_admin_site = MyAdminSite(name='myadmin')
