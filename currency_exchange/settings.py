"""
Django settings for currency_exchange project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = (
    os.environ.get(
        "SECRET_KEY",
        "django-insecure-v7wc=hy3e%qfz@q9+q%%6(i664vi5)u&bksjg2z1dq!#@20+n5",
    ),
)

ENVIRONMENT = os.environ.get(
    "ENVIRONMENT",
    "development",
)
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_filters",
    "django_celery_results",
    "django_celery_beat",
    "django_extensions",
]

CURRENCY_EXCHANGE_APPS = [
    "apps.core.apps.CoreConfig",
    "apps.exchange.apps.ExchangeConfig",
]

INSTALLED_APPS += CURRENCY_EXCHANGE_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "currency_exchange.urls"

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

WSGI_APPLICATION = "currency_exchange.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "currency_exchange"),
        "USER": os.environ.get("POSTGRES_USER", "postgres"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "postgres"),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        "ATOMIC_REQUESTS": True,
        "CONN_MAX_AGE": 60 * 10,
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa
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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "handlers": {
#         "console": {
#             "level": "DEBUG",
#             "class": "logging.StreamHandler",
#         },
#         "file": {
#             "level": "INFO",
#             "class": "logging.FileHandler",
#             "filename": "currency_data_loader.log",
#         },
#     },
#     "loggers": {
#         "root": {
#             "handlers": ["console"],
#             "level": "DEBUG",
#             "propagate": True,
#         },
#         # "django.db.backends": {
#         #     "handlers": ["console"],
#         #     "level": "DEBUG",
#         #     "propagate": False,
#         # },
#     },
# }


# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "filters": {
#         "info_filter": {
#             "()": "django.utils.log.CallbackFilter",
#             "callback": lambda record: record.levelno == logging.INFO,
#         },
#         "warning_filter": {
#             "()": "django.utils.log.CallbackFilter",
#             "callback": lambda record: record.levelno == logging.WARNING,
#         },
#         "error_filter": {
#             "()": "django.utils.log.CallbackFilter",
#             "callback": lambda record: record.levelno == logging.ERROR,
#         },
#         "critical_filter": {
#             "()": "django.utils.log.CallbackFilter",
#             "callback": lambda record: record.levelno == logging.CRITICAL,
#         },
#     },
#     "formatters": {
#         "standard": {
#             "class": "logging.Formatter",
#             "datefmt": "%Y-%m-%d %H:%M:%S",
#             "format": "[%(levelname)s] %(asctime)s  %(name)s - %(message)s",
#         },
#         "verbose": {
#             "format": (
#                 "{asctime} | {levelname:<8} | {name} | {processName}({process}) | "
#                 "{threadName} | {filename}:{lineno} | {message}"
#             ),
#             "style": "{",
#             "datefmt": "%Y-%m-%d %H:%M:%S",
#         },
#     },
#     "handlers": {
#         "console": {
#             "level": "DEBUG",
#             "class": "logging.StreamHandler",
#             "formatter": "standard",
#         },
#         "info_file": {
#             "level": "INFO",
#             "class": "logging.handlers.RotatingFileHandler",
#             "filename": BASE_DIR / "logs/info.log",
#             "maxBytes": 1024 * 1024 * 5,  # 5 MB
#             "backupCount": 20,
#             "encoding": "utf8",
#             "formatter": "verbose",
#             "filters": ["info_filter"],
#         },
#         "warning_file": {
#             "level": "WARNING",
#             "class": "logging.handlers.RotatingFileHandler",
#             "filename": BASE_DIR / "logs/warning.log",
#             "maxBytes": 1024 * 1024 * 5,  # 5 MB
#             "backupCount": 20,
#             "encoding": "utf8",
#             "formatter": "verbose",
#             "filters": ["warning_filter"],
#         },
#         "error_file": {
#             "level": "ERROR",
#             "class": "logging.handlers.RotatingFileHandler",
#             "filename": BASE_DIR / "logs/error.log",
#             "maxBytes": 1024 * 1024 * 5,  # 5 MB
#             "backupCount": 20,
#             "encoding": "utf8",
#             "formatter": "verbose",
#             "filters": ["error_filter"],
#         },
#         "critical_file": {
#             "level": "CRITICAL",
#             "class": "logging.handlers.RotatingFileHandler",
#             "filename": BASE_DIR / "logs/critical.log",
#             "maxBytes": 1024 * 1024 * 5,  # 5 MB
#             "backupCount": 20,
#             "encoding": "utf8",
#             "formatter": "verbose",
#             "filters": ["critical_filter"],
#         },
#         "worker_info_file": {
#             "level": "INFO",
#             "class": "logging.handlers.RotatingFileHandler",
#             "filename": BASE_DIR / "logs/workers/info.log",
#             "maxBytes": 1024 * 1024 * 5,  # 5 MB
#             "backupCount": 20,
#             "encoding": "utf8",
#             "formatter": "verbose",
#             "filters": ["info_filter"],
#         },
#         "worker_warning_file": {
#             "level": "WARNING",
#             "class": "logging.handlers.RotatingFileHandler",
#             "filename": BASE_DIR / "logs/workers/warning.log",
#             "maxBytes": 1024 * 1024 * 5,  # 5 MB
#             "backupCount": 20,
#             "encoding": "utf8",
#             "formatter": "verbose",
#             "filters": ["warning_filter"],
#         },
#         "worker_error_file": {
#             "level": "ERROR",
#             "class": "logging.handlers.RotatingFileHandler",
#             "filename": BASE_DIR / "logs/workers/error.log",
#             "maxBytes": 1024 * 1024 * 5,  # 5 MB
#             "backupCount": 20,
#             "encoding": "utf8",
#             "formatter": "verbose",
#             "filters": ["error_filter"],
#         },
#         "worker_critical_file": {
#             "level": "CRITICAL",
#             "class": "logging.handlers.RotatingFileHandler",
#             "filename": BASE_DIR / "logs/workers/critical.log",
#             "maxBytes": 1024 * 1024 * 5,  # 5 MB
#             "backupCount": 20,
#             "encoding": "utf8",
#             "formatter": "verbose",
#             "filters": ["critical_filter"],
#         },
#     },
#     "loggers": {
#         "django": {
#             "handlers": ["info_file", "warning_file", "error_file", "critical_file"]
#             if ENVIRONMENT in ["testing", "demo", "production"]
#             else ["console"],
#             "level": "DEBUG" if ENVIRONMENT == "development" else "WARNING",
#             "propagate": False,
#         },
#         "apps": {
#             "handlers": ["info_file", "warning_file", "error_file", "critical_file"]
#             if ENVIRONMENT in ["testing", "demo", "production"]
#             else ["console"],
#             "level": "DEBUG" if ENVIRONMENT == "development" else "INFO",
#             "propagate": False,
#         },
#         "apps.workers": {
#             "handlers": [
#                 "worker_info_file",
#                 "worker_warning_file",
#                 "worker_error_file",
#                 "worker_critical_file",
#             ]
#             if ENVIRONMENT in ["testing", "demo", "production"]
#             else ["console"],
#             "level": "DEBUG" if ENVIRONMENT == "development" else "INFO",
#             "propagate": False,
#         },
#     },
# }

# Cache
REDIS_CONNECTION_STRING = os.environ.get(
    "REDIS_CONNECTION_STRING", "redis://localhost:6379"
)

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_CONNECTION_STRING,  # noqa
    }
}

# cache key prefix
CACHE_KEY_PREFIX_AVAILABLE_CURRENCIES = "available_currencies"
CACHE_KEY_PREFIX_EXCHANGE_RATE = "exchange_rate"

# DRF settings

REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
}
