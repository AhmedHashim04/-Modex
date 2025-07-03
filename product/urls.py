from django.urls import path

from .views import (ProductDetailView, ProductListView)

app_name = "product"


urlpatterns = [
    path("", ProductListView.as_view(), name="products_list"),
    path("<slug:slug>/", ProductDetailView.as_view(), name="product_detail"),
    # path("compare/", CompareProductsView.as_view(), name="compare_products"),
    # path('<slug:slug>/view/', user_see_product, name="user_see_product"),
]
