"""What the service needs from its environment to start."""

from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent


# --- The environment -----------------------------------------------------------

env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
)
environ.Env.read_env(BASE_DIR / ".env")

# What signs anything Django signs. It has no default.
SECRET_KEY = env("DJANGO_SECRET_KEY")

DEBUG = env("DEBUG")
ALLOWED_HOSTS = env("ALLOWED_HOSTS")


# --- The application -----------------------------------------------------------

# No users, no sessions, no admin: Nexo's database is not ours to migrate into.
DJANGO_APPS: list[str] = []

THIRD_PARTY_APPS: list[str] = [
    "corsheaders",
    "rest_framework",
]

LOCAL_APPS: list[str] = [
    "contexts.consumption",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"


# --- The API -------------------------------------------------------------------

# DRF opens every route by default, and answers anonymous callers with a user
# model this service does not have.
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "EXCEPTION_HANDLER": "config.exception_handler.handle",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "contexts.consumption.infrastructure.api.authentication.ServiceTokenAuthentication",
    ],
    "UNAUTHENTICATED_USER": None,
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
}


# --- Who may ask ---------------------------------------------------------------

# What the billing server presents to be heard. It has no default.
SERVICE_TOKEN = env("SERVICE_TOKEN")


# --- Who may read it from a browser --------------------------------------------

CORS_ALLOW_ALL_ORIGINS = env.bool("CORS_ALLOW_ALL_ORIGINS", default=False)
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])


# --- The database --------------------------------------------------------------

# Nexo's own database. Only ever read from here.
DATABASES = {"default": env.db()}

DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)


# --- Language and time ---------------------------------------------------------

LANGUAGE_CODE = "es"

# A billing day is a UTC day: the monthly pre-invoices were cut that way.
TIME_ZONE = "UTC"

USE_I18N = True
USE_TZ = True


# --- Logs ----------------------------------------------------------------------

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "app": {"format": "{levelname} {asctime} {name} {message}", "style": "{"},
    },
    # The stream. The disk under a process is temporary.
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "app"},
    },
    "root": {"handlers": ["console"], "level": env("LOG_LEVEL", default="INFO")},
}


# --- The transport -------------------------------------------------------------

# Callers on the internal network may not speak TLS; whoever deploys decides.
FORCE_HTTPS = env.bool("FORCE_HTTPS", default=not DEBUG)

SECURE_SSL_REDIRECT = FORCE_HTTPS

# A year, and a browser remembers it.
SECURE_HSTS_SECONDS = 31_536_000 if FORCE_HTTPS else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = FORCE_HTTPS
SECURE_HSTS_PRELOAD = FORCE_HTTPS

# The proxy's word for how the visitor arrived.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
