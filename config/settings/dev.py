import os

from .base import *  # noqa: F403

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", os.getenv("SECRET_KEY", "django-insecure-development-key"))
DEBUG = os.getenv("DJANGO_DEBUG", os.getenv("DEBUG", "True")).lower() in ("true", "1")

env_hosts = os.getenv("DJANGO_ALLOWED_HOSTS", os.getenv("ALLOWED_HOSTS", ""))
if env_hosts:
    ALLOWED_HOSTS = [h.strip() for h in env_hosts.split(",") if h.strip()]
    if "testserver" not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append("testserver")
else:
    ALLOWED_HOSTS = ["127.0.0.1", "localhost", "testserver", "bahaa.mwheba.co.uk", "*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
