"""Models for twittertorss app."""

from django import forms
from google.appengine.ext import ndb


class User(ndb.Model):
  """Basic model for twitter users."""
  username = ndb.StringProperty()


class UserForm(forms.Form):
  """Basic form for editing users."""
  username = forms.CharField()
