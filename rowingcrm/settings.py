"""
Django settings for rowingcrm project.

Generated by 'django-admin startproject' using Django 2.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

import django_heroku
from decouple import config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', '')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'gtcrew-staging.herokuapp.com',
                 'gtcrew.herokuapp.com', 'app.gtcrew.com', 'gtcrew.com']

# Application definition

INSTALLED_APPS = [
    'team.apps.TeamConfig',
    'event.apps.EventConfig',
    'story.apps.StoryConfig',
    'asset.apps.AssetConfig',
    'feedback.apps.FeedbackConfig',
    'dal',
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'captcha',
    'django_cleanup',
    'cuser',
    'django_summernote',
    'tempus_dominus',
    'actstream.apps.ActstreamConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cuser.middleware.CuserMiddleware',
]

ROOT_URLCONF = 'rowingcrm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'rowingcrm.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Django-RECAPTCHA
RECAPTCHA_PUBLIC_KEY = config('RECAPTCHA_SITEKEY', '')
RECAPTCHA_PRIVATE_KEY = config('RECAPTCHA_SECRETKEY', '')
# SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']  # used during testing only

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

# STATIC_URL = '/static/'
# STATIC_ROOT = 'static_root/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME', '')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

AWS_LOCATION = 'static'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)

DEFAULT_FILE_STORAGE = 'rowingcrm.storage_backends.MediaStorage'

AWS_DEFAULT_ACL = 'public-read'

# SummerNote
X_FRAME_OPTIONS = 'SAMEORIGIN'
SUMMERNOTE_THEME = 'bs4'
SUMMERNOTE_CONFIG = {
    # 'iframe': False,
    'attachment_require_authentication': True,
}

# Activity Stream
SITE_ID = 1

# Import local_settings if local
try:
    from .local_settings import *
except ImportError:
    pass

LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = 'team:index'

# Activate Django-Heroku.
if not DEBUG:
    django_heroku.settings(locals())
