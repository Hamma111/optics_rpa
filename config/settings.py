import os.path
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from config.env_utils import get_env_variable

BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-#bygs457ci5a!dw*=x*kejk-#69yk-62yhvk&-dzi6^ne7p^n$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(get_env_variable("DEBUG")))
ENV = get_env_variable("ENV")

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    # default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third party package
    "django_celery_beat",
    "storages",
    "constance",
    "django_extensions",
    "django_filters",

    # custom apps
    "optics.core",
    "optics.rpa",
    "optics.users",
    "optics.submissions",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

AUTH_USER_MODEL = "users.User"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates", BASE_DIR / "static"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 'django.template.context_processors.static',  # this may cause issue later on
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": get_env_variable("DB_ENGINE"),
        "NAME": get_env_variable("DB_NAME"),
        "USER": get_env_variable("DB_USER"),
        "PASSWORD": get_env_variable("DB_PASSWORD"),
        "HOST": get_env_variable("DB_HOST"),
        "PORT": get_env_variable("DB_PORT"),
    },
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


STATIC_URL = '/django-static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REDIS_HOST = get_env_variable("REDIS_HOST")
REDIS_PORT = get_env_variable("REDIS_PORT")

# Celery Settings
CELERY_BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"
CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:{REDIS_PORT}"
CELERY_ACCEPT_CONTENT = [
    "application/json",
]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

# AWS Settings
AWS_ACCESS_KEY_ID = get_env_variable("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = get_env_variable("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = get_env_variable("AWS_STORAGE_BUCKET_NAME")
AWS_S3_ENDPOINT_URL = get_env_variable("AWS_S3_ENDPOINT_URL")
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}
AWS_MEDIA_FILES_LOCATION = "media-files"
AWS_DEFAULT_ACL = None
AWS_S3_VERIFY = True
AWS_S3_SIGNATURE_VERSION = 's3v4'
# AWS_S3_ADDRESSING_STYLE = 'virtual'
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

MEDIA_ROOT = BASE_DIR / "media"  # noqa
MEDIA_URL = f"https://{AWS_S3_ENDPOINT_URL}/{AWS_MEDIA_FILES_LOCATION}/"

# Constance settings
CONSTANCE_BACKEND = "constance.backends.redisd.RedisBackend"
CONSTANCE_REDIS_CONNECTION = f"{REDIS_HOST}://{REDIS_HOST}:{REDIS_PORT}/0"
CONSTANCE_REDIS_PREFIX = "constance:optics_rpa:"

from .constance import *

FILE_UPLOAD_HANDLERS = ['django.core.files.uploadhandler.TemporaryFileUploadHandler',]

LOGIN_URL = "users:login"

OPTICAL_PIA_USERID = get_env_variable("OPTICAL_PIA_USERID")
OPTICAL_PIA_PASSWORD = get_env_variable("OPTICAL_PIA_PASSWORD")
IEHP_LOGIN_ID = get_env_variable("IEHP_LOGIN_ID")
IEHP_PASSWORD = get_env_variable("IEHP_PASSWORD")


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {filename}:{lineno} {funcName} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {asctime} {filename}:{lineno} {funcName} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "debug.log",
            "formatter": "verbose",
            "backupCount": 10,
            "maxBytes": 1024 * 1024 * 100,  # 100 MB
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["console", "file"],
            "level": "INFO",
        },
        "celery": {
            "handlers": ["console", "file"],
            "level": "INFO",
        },
        "optics": {
            "handlers": ["console", "file"],
            "level": "INFO",
        },
    },
}
