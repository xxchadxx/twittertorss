"""Models for twittertorss app."""

import settings
import tweepy
from django import forms
from google.appengine.ext import ndb

# URL of a direct link to a tweet.
TWEET_LINK = 'https://twitter.com/{username}/status/{tweet_id}'


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
  last_tweet_id = ndb.StringProperty()
  created = ndb.DateTimeProperty(auto_now_add=True)
  updated = ndb.DateTimeProperty(auto_now=True)


class Tweet(ndb.Model):
  """Model representing a tweet."""
  tweet_id = ndb.StringProperty()
  text = ndb.StringProperty()
  tweet_time = ndb.DateTimeProperty()
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
        username=status.user.screen_name)


class UserForm(forms.Form):
  """Basic form for editing users."""
  username = forms.CharField()

  def clean(self):
    """Cleans the data for the UserForm."""
    cleaned_data = super(UserForm, self).clean()

    # Get the user's twitter id and ensure the username is in the correct case.
    api = OpenTwitterConnection()
    user = api.get_user(screen_name=cleaned_data['username'])
    cleaned_data['user_id'] = user.id_str
    cleaned_data['username'] = user.screen_name
    return cleaned_data
