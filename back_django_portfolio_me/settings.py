"""
Django settings for back_django_portfolio_me project.
"""

import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

# --------------------------------------------------
# Charger explicitement le .env
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")  # charge le .env à la racine du projet

# --------------------------------------------------
# Quick-start development settings
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "django-insecure-default-key")
DEBUG = os.getenv("DEBUG", "True") in ["True", "true", "1"]
# ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

ALLOWED_HOSTS = ["*"]
# --------------------------------------------------
# Applications installées
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "core",
    "corsheaders",
    "rest_framework_simplejwt.token_blacklist",
    "channels",
]

# --------------------------------------------------
# JWT config
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=7),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
}

# --------------------------------------------------
# Django REST Framework config
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}

# --------------------------------------------------
# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # Must be near the top
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

# --------------------------------------------------
# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# --------------------------------------------------
# WSGI / ASGI
WSGI_APPLICATION = "back_django_portfolio_me.wsgi.application"
ASGI_APPLICATION = "back_django_portfolio_me.asgi.application"
ROOT_URLCONF = "back_django_portfolio_me.urls"  # ← Ajoute ça ! (adapte si ton urls.py est ailleurs)

# --------------------------------------------------
# Channels (dev only)
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}

# --------------------------------------------------
# Base URL
BASE_URL = os.getenv("BASE_URL", "https://portfolio.unityfianar.site")
FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL", "http://localhost:5173")

# --------------------------------------------------
# CORS
CORS_ALLOW_HEADERS = [
    "content-type",
    "authorization",
    "x-csrftoken",
    "x-requested-with",
]
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")

CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",")
# --------------------------------------------------
# Database (MySQL local Windows)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DB_DATABASE"),
        "USER": os.getenv("DB_USERNAME"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST", "127.0.0.1"),
        "PORT": os.getenv("DB_PORT", "3306"),
        "CONN_MAX_AGE": None,
        # SSL désactivé pour Windows local
        #'OPTIONS': {'ssl': {'ssl-mode': 'REQUIRED'}},
    }
}

# --------------------------------------------------
# Auth & Passwords
AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend"]
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --------------------------------------------------
# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# --------------------------------------------------
# Static & Media
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
EXTERNAL_FILES_DIR = "/home/server/Téléchargements"

# --------------------------------------------------
# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") in ["True", "true", "1"]
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

# --------------------------------------------------
# Cache (utilisé pour les challenges WebAuthn — TTL 2 min)
# En production avec plusieurs workers Gunicorn, utiliser Redis :
#   pip install django-redis
#   BACKEND: 'django_redis.cache.RedisCache'
#   LOCATION: 'redis://127.0.0.1:6379/1'
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": os.path.join(BASE_DIR, ".django_cache"),
        "TIMEOUT": 300,
    }
}

# --------------------------------------------------
# WebAuthn / Face ID
# WEBAUTHN_RP_ID    → domaine exact du frontend (sans https://, sans port)
# WEBAUTHN_ORIGIN   → URL complète autorisée (avec protocole ET port si besoin)
WEBAUTHN_RP_ID = os.getenv("WEBAUTHN_RP_ID", "localhost")
WEBAUTHN_RP_NAME = os.getenv("WEBAUTHN_RP_NAME", "Portfolio Nilsen")
WEBAUTHN_ORIGIN = os.getenv("WEBAUTHN_ORIGIN", "http://localhost:5173")

# --------------------------------------------------
# Debug prints — DÉSACTIVÉS en production (ne jamais loguer des credentials)
if DEBUG:
    print("DB_DATABASE:", os.getenv("DB_DATABASE"))
    print("DB_USERNAME:", os.getenv("DB_USERNAME"))
