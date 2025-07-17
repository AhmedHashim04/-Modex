from django.urls import path

from . import views

app_name = "features"


urlpatterns = [
    path('collection/', views.CollectionDetailView.as_view(), name='collection_detail'),
    path('wishlist/', views.view_wishlist, name='wishlist'),
    path('wishlist/clear/', views.clear_wishlist, name='clear_wishlist'),
    path('wishlist/add/<slug:product_slug>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<slug:product_slug>/', views.remove_from_wishlist, name='remove_from_wishlist'),


]
