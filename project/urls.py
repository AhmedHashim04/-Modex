"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns
from home.views import HomeView

# رابط تغيير اللغة لازم يكون خارج i18n_patterns
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

# جميع المسارات القابلة للترجمة داخل i18n_patterns
urlpatterns += i18n_patterns(
    path('', HomeView.as_view(), name='home'),  # صفحة البداية
    path('accounts/', include("accounts.urls", namespace="accounts")),
    path('accounts/', include("allauth.urls")),
    path('products/', include("product.urls", namespace="product")),
    path('order/', include("order.urls", namespace="order")),
    path('feature/', include("features.urls", namespace="feature")),
    path('cart/', include("cart.urls", namespace="cart")),
    path('contact/', include("contact.urls", namespace="contact")),
    path('admin/', admin.site.urls),
    prefix_default_language=False,
)

# ملفات static/media في وضع التطوير
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# handler404 = 'home.views.handler404'
# handler500 = 'home.views.handler500'

    

