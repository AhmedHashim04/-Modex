"""
Django 5.1
"""

import os
from pathlib import Path
from decouple import config  

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY =config('SECRET_KEY')

INSTALLED_APPS = [
    "accounts",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.facebook",
    "home",
    "contact",
    "product",
    "cart.apps.CartConfig",
    "order.apps.OrderConfig",
    'debug_toolbar',
    'django_ratelimit',
    "widget_tweaks",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django.contrib.sites',
    'django.contrib.humanize',

]


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  
    'allauth.account.auth_backends.AuthenticationBackend', 
]

ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_ADAPTER = 'project.adapters.NoNewUsersAccountAdapter'

LOGIN_REDIRECT_URL = '/' 
LOGOUT_REDIRECT_URL = "/"



MIDDLEWARE = [
    'project.rate_limit_logging.RatelimitLoggingMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    'django.middleware.locale.LocaleMiddleware',
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    'django_ratelimit.middleware.RatelimitMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

CACHE_METRICS = {
    'EXPORT': 'prometheus',  # يدعم أيضًا 'stdout' أو 'datadog'
}

RATELIMIT_VIEW='home.views.RateLimitExceeded'
ROOT_URLCONF = "project.urls"

WSGI_APPLICATION = "project.wsgi.application"


SITE_ID = 2

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# LANGUAGE_CODE = "en-us"
LANGUAGE_CODE = 'ar'
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ('ar', 'Arabic'),
    ('en', 'English'),
]


CRISPY_TEMPLATE_PACK = "bootstrap4"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


CART_SESSION_ID = "cart"


RATELIMIT_ENABLE = True
RATELIMIT_USE_CACHE = "default"

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
        'APP': {
            'client_id': config('GOOGLE_CLIENT_ID'),
            'secret': config('GOOGLE_CLIENT_SECRET'),
            'key': ''
        }
    }
}


SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = 'Your Shop <%s>' % config('DEFAULT_FROM_EMAIL')
STORE_OWNER_EMAIL = config('STORE_OWNER_EMAIL')
SHIPPING_EMAIL = config('SHIPPING_EMAIL')
