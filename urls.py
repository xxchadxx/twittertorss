"""Urls for twittertorss app."""

from django.conf.urls import defaults
from django.views import generic
from controllers import controllers
from model import model

# Url patterns
urlpatterns = defaults.patterns(
    '',
    defaults.url(
        r'^add/$', controllers.CreateUser.as_view(
            template_name='add.html', form_class=model.UserForm,
            model=model.User, success_url='/'),
        name='add'),
    defaults.url(
        r'^delete/(?P<slug>\w+)/$', controllers.DeleteUser.as_view(
            model=model.User, success_url='/', slug_field='username'),
        name='delete'),
    defaults.url(
        r'^rss/(?P<username>\w+)/$', model.TweetFeed(), name='rss'),
    defaults.url(
        r'^tweets/$', controllers.GetTweets.as_view(
            template_name='tweets.html'),
        name='tweets'),
    defaults.url(
        r'^users/$', controllers.RefreshUsers.as_view(
            template_name='users.html'),
        name='users'),
    defaults.url(
        r'^$', generic.ListView.as_view(
            template_name='index.html', context_object_name='user_list',
            queryset=lambda: sorted(model.User.query(), key=lambda x: x.name.lower())),
        name='index'),
)
