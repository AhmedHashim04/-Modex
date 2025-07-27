from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'trader',
        'USER': 'ahmed',
        'PASSWORD': 'MyS3cur3Pass',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
MIDDLEWARE +=     'project.middleware.TimerMiddleware',

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs/app.log",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
INTERNAL_IPS = [
    '127.0.0.1',
]

ALLOWED_HOSTS = []

DEBUG = True

# python manage.py migrate --settings=project.settings.production
# python manage.py runserver --settings=project.settings.production
# python manage.py collectstatic --settings=project.settings.production
