from .base import *  # noqa: F403

SECRET_KEY = "django-insecure-development-key"
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "testserver"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
