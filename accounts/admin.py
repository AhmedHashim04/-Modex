from django.contrib import admin
from .models import Profile
from project.admin import custom_admin_site

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address', 'governorate')
    search_fields = ('user__username', 'user__email', 'phone', 'address')
    list_filter = ('governorate',)
    
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
User = get_user_model()

custom_admin_site.register(Profile, ProfileAdmin)
custom_admin_site.register(User, UserAdmin)