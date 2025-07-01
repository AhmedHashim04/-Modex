from django.urls import path

from .views import SendEmailView

app_name = "contact"


urlpatterns = [
    path("", SendEmailView.as_view(), name="contact"),
]
