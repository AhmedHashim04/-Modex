from django.urls import path
from .views import profile_view, edit_profile, clear_wishlist, view_wishlist, toggle_wishlist, remove_wishlist

app_name = 'accounts'

urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('profile/wishlist/', view_wishlist, name='wishlist'),
    path('profile/wishlist/<slug:slug>/remove/', remove_wishlist, name='remove_wishlist'),
    path('profile/wishlist/toggle/', toggle_wishlist, name='toggle_wishlist'),
    path('profile/wishlist/clear/', clear_wishlist, name='clear_wishlist'),
    path('profile/edit/', edit_profile, name='edit_profile'),
]

