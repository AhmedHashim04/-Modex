from decouple import config  
from pathlib import Path
from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"



MIDDLEWARE += [
    'project.middleware.FullCPUMeasureMiddleware',
    'project.middleware.CPUMeasureMiddleware',
]
INTERNAL_IPS = [
    '127.0.0.1',
]

ALLOWED_HOSTS = []



LOCALE_PATHS = [
    BASE_DIR / 'locale',
]


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [ "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "project.context_module.global_context",
            ],
        },
    },
]


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / 'staticfiles'



# python manage.py migrate --settings=project.settings.dev
# python manage.py runserver --settings=project.settings.dev
# python manage.py collectstatic --settings=project.settings.dev

# python manage.py createsuperuser --settings=project.settings.dev
