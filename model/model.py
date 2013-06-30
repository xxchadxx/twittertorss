"""Models for twittertorss app."""

import settings
import tweepy
from django import forms
from django.contrib.syndication import views
from django.utils import html
from google.appengine.ext import ndb

# URLs of direct links to a user and a tweet.
USER_LINK = u'https://twitter.com/{username}'
TWEET_LINK = u'https://twitter.com/{username}/status/{tweet_id}'


def OpenTwitterConnection():
  """Opens a connection to the twitter api."""
  auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
  auth.set_access_token(
      settings.ACCESS_TOKEN_KEY, settings.ACCESS_TOKEN_SECRET)
  return tweepy.API(auth)


class User(ndb.Model):
  """Basic model for twitter users."""
  user_id = ndb.StringProperty()
  username = ndb.StringProperty()
  name = ndb.StringProperty()
  last_tweet_id = ndb.StringProperty()
  created = ndb.DateTimeProperty(auto_now_add=True)
  updated = ndb.DateTimeProperty(auto_now=True)

  @property
  def link(self):
    """Returns a direct link to this user."""
    return USER_LINK.format(username=self.username)


class UserForm(forms.Form):
  """Basic form for editing users."""
  username = forms.CharField()

  def clean(self):
    """Cleans the data for the UserForm."""
    cleaned_data = super(UserForm, self).clean()

    # Get the user's twitter id and name, and ensure the username is in the
    # correct case by pulling it from the user object.
    api = OpenTwitterConnection()
    user = api.get_user(screen_name=cleaned_data['username'])
    cleaned_data['user_id'] = user.id_str
    cleaned_data['username'] = user.screen_name
    cleaned_data['name'] = user.name
    return cleaned_data


class Tweet(ndb.Model):
  """Model representing a tweet."""
  tweet_id = ndb.StringProperty()
  text = ndb.StringProperty()
  tweet_time = ndb.DateTimeProperty()
  user_id = ndb.StringProperty()
  username = ndb.StringProperty()
  created = ndb.DateTimeProperty(auto_now_add=True)
  updated = ndb.DateTimeProperty(auto_now=True)

  @property
  def link(self):
    """Returns a direct link to this tweet."""
    return TWEET_LINK.format(username=self.username, tweet_id=self.tweet_id)

  @classmethod
  def CreateFromStatus(cls, status):
    """Create and return an object based on a status from the Twitter API."""
    return cls(
        tweet_id=status.id_str, text=status.text, tweet_time=status.created_at,
        user_id=status.user.id_str, username=status.user.screen_name)


class TweetFeed(views.Feed):
  """Class representing an RSS feed of a list of tweets."""

  def get_object(self, request, username):
    return User.query(User.username == username).get()

  def title(self, user):
    """Returns the title of the feed."""
    return u'{name} Twitter Feed'.format(name=user.name)

  def description(self, user):
    """Returns the description of the feed."""
    return u'RSS feed of tweets for {username}.'.format(username=user.username)

  def link(self, user):
    """Returns the link of the feed."""
    return user.link

  def items(self, user):
    """Returns the list of tweets for the feed."""
    return Tweet.query(Tweet.user_id == user.user_id).order(
        -Tweet.tweet_time).fetch(20)

  def item_title(self, tweet):
    """Returns the title of a tweet."""
    return u'{username}: {text}'.format(
        username=tweet.username, text=tweet.text)

  def item_description(self, tweet):
    """Returns the description of a tweet."""
    return html.urlize(tweet.text)

  def item_link(self, tweet):
    """Returns the link of a tweet."""
    return tweet.link
