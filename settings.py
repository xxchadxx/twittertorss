"""Settings for twittertorss app."""

import os
import local_settings

LANGUAGE_CODE = 'en-us'

SECRET_KEY = local_settings.SECRET_KEY

DEBUG = local_settings.DEBUG
TEMPLATE_DEBUG = DEBUG

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
)

MIDDLEWARE_CLASSES = (
    'google.appengine.ext.ndb.django_middleware.NdbDjangoMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
)

TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

LOGIN_REDIRECT_URL = '/'

ROOT_URLCONF = 'urls'
