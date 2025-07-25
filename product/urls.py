from django.urls import path

from .views import ProductDetailView, ProductListView

app_name = "product"

urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path("<slug:slug>/", ProductDetailView.as_view(), name="product_detail"),
]
