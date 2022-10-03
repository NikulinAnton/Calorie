"""
Django settings for calories project.

Generated by 'django-admin startproject' using Django 4.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv


load_dotenv()


def get_env(variable_name, default=None):
    value = os.getenv(variable_name, default)
    if value is None:
        raise ValueError(f"{variable_name} is not not presented in environment variables. Check your .env file")
    if str(value).lower() in ("true", "false"):
        return str(value).lower() == "true"
    return value

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_env("DEBUG", "False")

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    'django_paranoid',
    "drf_spectacular",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "calories.urls"

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

WSGI_APPLICATION = "calories.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {"default": dj_database_url.config(conn_max_age=600)}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DEFAULT_RENDERER_CLASSES = ("rest_framework.renderers.JSONRenderer",)

REST_FRAMEWORK = {
    "DEFAULT_THROTTLE_RATES": {"loginAttempts": "10/hr", "anon": "10000/day", "user": "10000/day"},
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "DEFAULT_RENDERER_CLASSES": DEFAULT_RENDERER_CLASSES,
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DATE_INPUT_FORMATS": [
        ("%Y-%m-%d"),
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "PAGE_SIZE": 50,
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "ORDERING_PARAM": "ordering",
}

if DEBUG:
    REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"].append("rest_framework.authentication.BasicAuthentication")

# https://drf-spectacular.readthedocs.io
SPECTACULAR_SETTINGS = {
    "TITLE": "Calories API",
    "DESCRIPTION": "Backend for Calories project",
    "VERSION": "3.0.0",
    "SCHEMA_PATH_PREFIX": r"/api/v1/",
}


AUTH_USER_MODEL = "core.CUser"

NUTRITION_API_KEY = get_env("NUTRITION_API_KEY")