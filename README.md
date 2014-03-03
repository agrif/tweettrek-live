tweetTrek Live Updater
======================

This is a small [flask][] application that uses [tweepy][] and
[flask-sockets][] to provide a simple real-time feed of [tweetTrek][]
tweets. It's packaged as a [Heroku][] application, and can be easily
modified to do other sorts of live feeds.

 [flask]: http://flask.pocoo.org/
 [tweepy]: https://github.com/tweepy/tweepy
 [flask-sockets]: http://kennethreitz.org/introducing-flask-sockets/
 [tweetTrek]: https://medium.com/p/8041e52fa832
 [Heroku]: https://dashboard.heroku.com/apps
 [gunicorn]: http://gunicorn.org/

Customization
-------------

To change the feed keyword, find the line in *livetweets.py* that
looks like:

    relay = Relay(track=['tweetTrek'])

and modify the list to contain your keywords. You can also follow users:

    relay = Relay(follow=['agrif'])

You'll also want to modify the files in `static/` and `templates/`.

Running the Test Server
-----------------------

To run a local test server:

 * Install all the packages found in *requirements.txt*:
   
        pip install -r requirements.txt
 
 * Set up the following environment variables:
   * `TWITTER_API_KEY`
   * `TWITTER_API_SECRET`
   * `TWITTER_ACCESS_TOKEN`
   * `TWITTER_ACCESS_SECRET`
 
 * Start the app with [gunicorn][]:
 
        gunicorn -k flask_sockets.worker livetweets:app

Deploy to Heroku
----------------

Deployment is much like any other Heroku app, documented elsewhere. However, you need to remember to set up the above environment variables with `heroku config:set`, and you also need to enable websockets:

    heroku labs:enable websockets

That's it!
