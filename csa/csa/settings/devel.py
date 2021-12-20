import os
from .base import *

DEBUG = True

ALLOWED_HOSTS = [
    "localhost",
    "192.168.1.176",
    "127.0.0.1:8000",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "database",
        "USER": "root",
        "PASSWORD": "clave",
        "HOST": "172.17.0.2",
        "PORT": "",
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
}


INSTALLED_APPS += ("debug_toolbar",)
INTERNAL_IPS = ("127.0.0.1",)

MIDDLEWARE += ("debug_toolbar.middleware.DebugToolbarMiddleware",)


CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8001",
    "http://192.168.1.176:8001",
]

# CORS_ORIGIN_ALLOW_ALL = DEBUG

# EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
# EMAIL_FILE_PATH = "/tmp/app-messages"  # change this to a proper location

# CELERY
REDIS_HOST = "redis-server"
CELERY_BROKER_URL = "redis://{}:6379/0".format(REDIS_HOST)

MAX_COMMENTS_PER_TIME = (500, 15)  # 5 COMMENTS X 15 MINUTES

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_HOST = "smtp.server.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "username@domain.es"
EMAIL_HOST_PASSWORD = "password"
EMAIL_USE_SSL = False
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "username@domain.es"
