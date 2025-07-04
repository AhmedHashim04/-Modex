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

# <h2>سجل دخول باستخدام</h2>
# <a href="{% url 'social:begin' 'google-oauth2' %}?next=/">Google</a><br>
# <a href="{% url 'social:begin' 'facebook' %}?next=/">Facebook</a>

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),  
    path("", include("product.urls", namespace="product")),
    path("order/", include("order.urls", namespace="order")),
    path("feature/", include("features.urls", namespace="feature")),
    path("cart/", include("cart.urls", namespace="cart")),
    path("contact/", include("contact.urls", namespace="contact")),
    path("payment/", include("payment.urls", namespace="payment")),
    # path('coupon/'  ,include('coupon.urls',namespace='coupon')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handler404 = 'home.views.handler404'
# handler500 = 'home.views.handler500'
