from django.urls import path
from .views import profile_view, edit_profile, check_profile_completion

app_name = 'accounts'
urlpatterns = [

    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('check-profile/', check_profile_completion, name='check_profile_completion'),
]
