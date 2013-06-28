"""Crons for twittertorss app."""

import logging
import settings
import tweepy
from django.views import generic
from model import model


class GetTweets(generic.TemplateView):
  """Cron job handler to get the latest tweets."""
  tweet_count = 0
  user_count = 0

  def get_context_data(self, **kwargs):
    """Gets additional context for the template."""
    context = super(GetTweets, self).get_context_data(**kwargs)
    context['tweet_count'] = self.tweet_count
    context['user_count'] = self.user_count
    return context

  def get(self, *args, **kwargs):
    """Function to get the tweets and store them, then display the status."""
    # Open connection to twitter api.
    auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    auth.set_access_token(
        settings.ACCESS_TOKEN_KEY, settings.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    # Get the statuses for each user.
    users = tuple(model.User.query())
    self.user_count = len(users)
    for user in users:
      statuses = api.user_timeline(
          screen_name=user.username, since_id=user.last_tweet_id)
      self.tweet_count += len(statuses)

      # Save the statuses to the DB.
      for status in statuses:
        tweet = model.Tweet.CreateFromStatus(status)
        tweet.put()

      if statuses:
        # Update the last_tweet_id of this user.
        user.last_tweet_id = statuses[0].id_str
        user.put()

    logging.info('%s tweets from %s users saved to DB.', self.tweet_count,
                 self.user_count)
    return super(GetTweets, self).get(*args, **kwargs)
