from allauth.account.adapter import DefaultAccountAdapter
from django.forms import ValidationError
from django.contrib import messages

class NoNewUsersAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return request.path.startswith("/accounts/google/")