from django.urls import path
from . import views

urlpatterns = [

    path('profile/', views.profile_view, name='profile'),
    path('update_profile/', views.profile_view, name='profile'),
]
