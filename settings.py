"""Settings for twittertorss app."""

import os

LANGUAGE_CODE = 'en-us'

SECRET_KEY = '1-b8om^fl2r6v^ot$e^=nn+!jplr^_tv_a)id6hjeg+n-namq('

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
)

MIDDLEWARE_CLASSES = (
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

DEBUG = True
TEMPLATE_DEBUG = DEBUG
