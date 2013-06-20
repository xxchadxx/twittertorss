"""Main.py for twittertorss app."""

import logging
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

# Force Django to reload its settings.
from django.conf import settings

from django.core.handlers import wsgi
from django.core import signals
from django import db
from django import dispatch

def log_exception(*args, **kwargs):
    logging.exception('Exception in request:')

signal = dispatch.Signal()

# Log errors.
signal.connect(log_exception, signals.got_request_exception)

# Unregister the rollback event handler.
signal.disconnect(db._rollback_on_exception, signals.got_request_exception)

app = wsgi.WSGIHandler()
