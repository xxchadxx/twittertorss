twittertorss
============

Stores tweets from a whitelist of users in the app engine datastore, then
outputs those tweets as an RSS feed. I created this to continue following
a handful of Twitter users in my RSS reader after Twitter shut off RSS support
when they turned off API v1.

All of the code I wrote (basically everything except tweety) is licensed under
the "do whatever the hell you want with it" license.  Seriously this only took
me a few hours, so go ahead and copy it all you want if this will be useful to
you.

If you want to start up your own version to follow twitter users in your
favorite feed reader, follow these instructions.
1. Clone the code.
2. Register an app engine app.
3. Update app.yaml, changing the application name to your app engine app.
4. Register as a Twitter developer and get your oauth credentials. There should
   be 4 (consumer key and secret, access token key and secret).
5. Generate a Django secret key (just Google [Django secret key generator]).
6. Create a file in the top level directory called local_settings.py.
7. Add these 6 variables to local_settings.py:
   - DEBUG (boolean True or False)
   - SECRET_KEY (the Django secrete key, as a string)
   - CONSUMER_KEY (Twitter consumer key, as a string)
   - CONSUMER_SECRET (Twitter consumer secret, as a string)
   - ACCESS_TOKEN_KEY (Twitter access token key, as a string)
   - ACCESS_TOKEN_SECRET (Twitter access token secret, as a string)
8. Deploy to app engine, add a user, and click on the username once you've
   added them to get the RSS feed link.

As long as you don't follow dozens of people who tweet hundreds of times per
day, you should fall well within the free quotas for both App Engine and the
Twitter API.

Enjoy!
