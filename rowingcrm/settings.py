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
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', '')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# Domains and Hosts
DOMAIN = os.environ.get('DOMAIN', '')

DOMAIN_ALIASES = [
    d.strip()
    for d in os.environ.get('DOMAIN_ALIASES', '').split(',')
    if d.strip()
]

ALLOWED_HOSTS = [DOMAIN] + DOMAIN_ALIASES

SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True') == 'True'
SECURE_SSL_HOST = DOMAIN

# Application definition

INSTALLED_APPS = [
    'gtcrew',  # location of the Wagtail Page models
    'roster',
    'person',
    'award',
    'shell',
    'team.apps.TeamConfig',
    'event.apps.EventConfig',
    'story.apps.StoryConfig',
    'asset.apps.AssetConfig',
    'feedback.apps.FeedbackConfig',
    'campaign.apps.CampaignConfig',

    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.contrib.modeladmin',
    'wagtail.contrib.styleguide',
    'wagtail.contrib.settings',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail',

    'wagtailcaptcha',
    'wagtailautocomplete',
    'robots',
    'wagalytics',
    'wagtailfontawesome',

    'taggit',
    'modelcluster',

    'dal',
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'storages',
    'captcha',
    'django_cleanup',
    'cuser',
    'django_summernote',
    'tempus_dominus',
    'actstream.apps.ActstreamConfig',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
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
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
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
                # allow access to wagtail settings in templates
                'wagtail.contrib.settings.context_processors.settings',
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

# Authentication Backends
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Default auto field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django-RECAPTCHA
RECAPTCHA_PUBLIC_KEY = config('RECAPTCHA_SITEKEY', '')
RECAPTCHA_PRIVATE_KEY = config('RECAPTCHA_SECRETKEY', '')
# SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']  # used during testing only

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
]

if config('USE_S3', False):
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', '')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY', '')
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME', '')
    AWS_S3_CUSTOM_DOMAIN = config('AWS_S3_CUSTOM_DOMAIN', '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME)
    AWS_S3_ENDPOINT_URL = config('AWS_S3_ENDPOINT_URL', None)

    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }

    AWS_LOCATION = 'static'
    STATICFILES_STORAGE = 'rowingcrm.storage_backends.StaticStorage'
    STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)

    DEFAULT_FILE_STORAGE = 'rowingcrm.storage_backends.MediaStorage'

    AWS_DEFAULT_ACL = 'private'
else:
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    STATIC_URL = '/static/'

    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'

# SummerNote
X_FRAME_OPTIONS = 'SAMEORIGIN'
SUMMERNOTE_THEME = 'bs4'
SUMMERNOTE_CONFIG = {
    # 'iframe': False,
    'attachment_require_authentication': True,
}

# Activity Stream
SITE_ID = 1

# Email Backend
DEFAULT_FROM_EMAIL = os.getenv('FROM_EMAIL', 'webmaster@gtcrew.com')
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY', '')
if SENDGRID_API_KEY:
    EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Wagtail
WAGTAIL_SITE_NAME = 'Georgia Tech Rowing'
WAGTAILEMBEDS_RESPONSIVE_HTML = True
WAGTAILADMIN_GLOBAL_PAGE_EDIT_LOCK = True
WAGTAIL_FRONTEND_LOGIN_URL = '/account/login'
WAGTAILADMIN_RICH_TEXT_EDITORS = {
    'default': {
        'WIDGET': 'wagtail.admin.rich_text.DraftailRichTextArea',
        'OPTIONS': {
            'features': ['h1', 'h2', 'h3', 'h4', 'bold', 'italic',
                         'strikethrough', 'ol', 'ul', 'hr',
                         'link', 'document-link', 'image', 'embed']
        }
    },
}

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
WAGTAILADMIN_BASE_URL = DOMAIN

# Import local_settings if local
try:
    from .local_settings import *
except ImportError:
    pass

# Google Analytics
GOOGLE_ANALYTICS_CODE = config('GOOGLE_ANALYTICS_CODE', '')
GA_VIEW_ID = config('GA_VIEW_ID', '')
GA_KEY_CONTENT = config('GA_KEY_CONTENT', '')

# Login
LOGIN_URL = WAGTAIL_FRONTEND_LOGIN_URL

# where requests are redirected after login when the LoginView doesn't get a next GET parameter.
LOGIN_REDIRECT_URL = 'wagtailadmin_home'

PUBLIC_GROUP_ID = 2  # editors

# Allauth settings
ACCOUNT_FORMS = {'signup': 'gtcrew.forms.AllauthSignupForm'}
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
# ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_USERNAME_BLACKLIST = ["admin", "god", "gtcrew"]

# Activate Django-Heroku.
if not DEBUG:
    django_heroku.settings(locals())
