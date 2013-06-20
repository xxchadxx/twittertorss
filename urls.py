"""Urls for twittertorss app."""

from django.conf.urls import defaults
from django.views.generic import base

urlpatterns = defaults.patterns('',
    (r'^$', base.TemplateView.as_view(template_name='index.html')),
)
