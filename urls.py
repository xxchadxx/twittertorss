"""Urls for twittertorss app."""

from django.conf.urls import defaults
from django.views.generic import list as generic_list
from model import model

urlpatterns = defaults.patterns('',
    (r'^$', generic_list.ListView.as_view(
        template_name='index.html', context_object_name='user_list',
        queryset=model.User.query())),
)
