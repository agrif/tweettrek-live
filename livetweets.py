import gevent
import gevent.monkey
gevent.monkey.patch_all()

import os
import sys
import json
import logging
import random

from flask import Flask, render_template
from flask_sockets import Sockets
import tweepy

class config:
    api_key = os.environ['TWITTER_API_KEY']
    api_secret = os.environ['TWITTER_API_SECRET']
    access_token = os.environ['TWITTER_ACCESS_TOKEN']
    access_secret = os.environ['TWITTER_ACCESS_SECRET']

app = Flask(__name__)
app.debug = 'DEBUG' in os.environ

sockets = Sockets(app)

class Relay(tweepy.StreamListener):
    def __init__(self, track=[], follow=[]):
        auth = tweepy.OAuthHandler(config.api_key, config.api_secret)
        auth.set_access_token(config.access_token, config.access_secret)
        self.api = tweepy.API(auth)        
        
        self.stream = tweepy.Stream(auth, self)
        self.track = track
        self.follow = follow
        
        self.clients = []
        
    def run(self):
        try:
            self.stream.filter(track=self.track, follow=self.follow)
        except Exception, e:
            logging.exception('error during tweepy filter!')
            self.stream.disconnect()
    
    def start(self):
        gevent.spawn(self.run)
    
    def register(self, client):
        self.clients.append(client)
    
    def send(self, client, data):
        try:
            client.send(json.dumps(data))
        except Exception:
            self.clients.remove(client)
    
    def on_error(self, status_code):
        logging.error('tweepy error: ' + str(status_code))
        return False
    
    def on_timeout(self):
        logging.warning('tweepy timeout, sleeping for 60 seconds...')
        gevent.sleep(60)

    def on_status(self, status):
        retweeted = 'retweeted_status' in dir(status)
        if retweeted:
            return

        data = {}
        data['text'] = status.text
        data['screen_name'] = status.author.screen_name
        data['name'] = status.author.name
        data['author_url'] = 'http://twitter.com/' + status.author.screen_name
        data['author_image'] = status.author.profile_image_url
        data['url'] = data['author_url'] + '/status/' + status.id_str
        data['id'] = status.id_str
        data['created_at'] = status.created_at.isoformat()
        
        #print data
        
        for client in self.clients:
            gevent.spawn(self.send, client, data)
    
    def on_delete(self, status_id, user_id):
        pass
    
    def on_limit(self, track):
        logging.warning('tweepy limit: ' + str(track))

relay = Relay(track=['tweetTrek'])
relay.start()

@app.route('/')
def index():
    return render_template('index.html', bgnum=random.randint(0, 2))

@sockets.route('/live')
def live(ws):
    relay.register(ws)
    while not ws.closed:
        gevent.sleep(0.1)
