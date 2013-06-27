"""Urls for twittertorss app."""

from django.conf.urls import defaults
from django.views.generic import list as generic_list
from controllers import controllers
from cron import cron
from model import model

# Generic url patterns
urlpatterns = defaults.patterns(
    '',
    defaults.url(
        r'^add/$', controllers.CreateView.as_view(
            template_name='add.html', form_class=model.UserForm,
            model=model.User, success_url='/'),
        name='add'),
    defaults.url(
        r'^delete/(?P<slug>\w+)/$', controllers.DeleteView.as_view(
            model=model.User, success_url='/', slug_field='username'),
        name='delete'),
    defaults.url(
        r'^$', generic_list.ListView.as_view(
            template_name='index.html', context_object_name='user_list',
            queryset=model.User.query().order(model.User.username)),
        name='index'),
)

# Cron patterns.
urlpatterns += defaults.patterns(
    '',
    defaults.url(
        r'^tweets/$', cron.GetTweets.as_view(template_name='tweets.html'),
        name='tweets'),
)
