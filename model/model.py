"""Models for twittertorss app."""

from django import forms
from google.appengine.ext import ndb


class User(ndb.Model):
  """Basic model for twitter users."""
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

  @classmethod
  def CreateFromStatus(cls, status):
    """Create and return an object based on a status from the Twitter API."""
    return cls(
        tweet_id=status.id_str, text=status.text, tweet_time=status.created_at,
        username=status.user.screen_name)


class UserForm(forms.Form):
  """Basic form for editing users."""
  username = forms.CharField()
