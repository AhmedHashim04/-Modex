from django.urls import path

from . import views

app_name = "features"


urlpatterns = [
    path("collections/<str:slug>/",views.CollectionDetailView.as_view(),name="collection_detail",
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),

    ),
]
