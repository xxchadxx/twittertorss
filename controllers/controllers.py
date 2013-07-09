"""Controllers for twittertorss app."""

import logging
from django import shortcuts
from django.views import generic
from model import model


def GetTweetsForUser(user):
  """Gets the most recent tweets for a user and saves them to the DB."""
  api = model.OpenTwitterConnection()
  statuses = api.user_timeline(
      screen_name=user.username, since_id=user.last_tweet_id)

  # Save the statuses to the DB.
  for status in statuses:
    tweet = model.Tweet.CreateFromStatus(status)
    tweet.put()

  if statuses:
    # Update the last_tweet_id of this user.
    user.last_tweet_id = statuses[0].id_str
    user.put()

  return len(statuses)


class CreateUser(generic.CreateView):
  """Basic controller for creating user objects."""

  def get(self, request):
    """Process a get request."""
    return shortcuts.render(
        request, self.template_name, {'form': self.form_class()})

  def post(self, request):
    """Process a post submission."""
    form = self.form_class(request.POST)
    # If the form is valid, save the corresponding user and redirect.
    if form.is_valid():
      user = self.model(**form.cleaned_data)
      user.put()
      tweet_count = GetTweetsForUser(user)
      logging.info('Added %s and got %s tweets.', user.username, tweet_count)
      return shortcuts.redirect(self.success_url)

    # Form isn't valid, so display the template with the form.
    else:
      return shortcuts.render(request, self.template_name, {'form': form})


class DeleteUser(generic.DeleteView):
  """Basic controller for deleting user objects."""

  def post(self, request, slug=None):
    """Process a post submission."""
    user = self.model.query(getattr(self.model, self.slug_field) == slug).get()
    user.key.delete()

    # Delete tweets for the user.
    tweets = tuple(model.Tweet.query(model.Tweet.username == user.username))
    for tweet in tweets:
      tweet.key.delete()

    logging.info('Deleted %s and all associated tweets.', user.username)
    return shortcuts.redirect(self.success_url)


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
    # Get the statuses for each user.
    users = tuple(model.User.query())
    self.user_count = len(users)
    self.tweet_count = sum(GetTweetsForUser(user) for user in users)

    logging.info('%s tweets from %s users saved to DB.', self.tweet_count,
                 self.user_count)
    return super(GetTweets, self).get(*args, **kwargs)


class RefreshUsers(generic.TemplateView):
  """Cron job handler to ensure user data (name / profile pic) is up to date."""
  user_count = 0

  def get_context_data(self, **kwargs):
    """Gets additional context for the template."""
    context = super(RefreshUsers, self).get_context_data(**kwargs)
    context['user_count'] = self.user_count
    return context

  def get(self, *args, **kwargs):
    """Function to update everyone's data."""
    api = model.OpenTwitterConnection()

    # Get the info for each user.
    users = tuple(model.User.query())
    self.user_count = len(users)
    for user in users:
      new_user = api.get_user(user_id=user.user_id)
      user.username = new_user.screen_name
      user.name = new_user.name
      user.profile_pic = new_user.profile_image_url
      user.put()

    logging.info('Updated info for all %s users.', self.user_count)
    return super(RefreshUsers, self).get(*args, **kwargs)
