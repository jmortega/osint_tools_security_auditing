#!/usr/bin/env python
# -*- coding: utf-8 -*-

# encoding=utf8
import sys

##################################################################

from time import sleep
from sys import exit
import tweepy
import json
from pytagcloud import create_tag_image, make_tags
import re
from pytagcloud.lang.stopwords import StopWords
from operator import itemgetter

########## CONFIG ##########
consumer_token = 'cRz70QuhNCGvFMlFHy3ARekMY'
consumer_secret = 'WBdhkig3nZ5DTFZS0UKN0k2HnmwgbQ39xQRN6kWzeE2DfvYztg'
access_token = '201832916-lLrZ1Qw4D5zQZii0k3RgOxuY0ymnyJfPkQSXu1sc'
access_secret = 'YLKNQfqIfgN9PK8IwYBd3TsSI3fkl1pfXgUkM3aP9Xgl8'
############################

def OAuth():
   
   cToken = consumer_token
   cSecret = consumer_secret
   aToken = access_token
   aSecret = access_secret

   # Instantiate authorization manager
   auth = tweepy.OAuthHandler(cToken, cSecret)

   if aToken == '' or aSecret == '':
      try:
         redirect_url = auth.get_authorization_url()
         print('Application needs to be authorized: {0}'.format(redirect_url))
      except tweepy.TweepError:
         print('Error in the token request.')
         
      aToken = auth.access_token.key
      aSecret = auth.access_token.secret
      
      log('Your access_token: {0}'.format(aToken))
      log('Your access_secret: {0}'.format(aSecret))

   # set values for auth token and secret
   auth.set_access_token(aToken, aSecret)

   return (tweepy.API(auth), auth)


def getTrends(woeid=1):   
   trends = api.trends_place(1)[0]['trends']
   
   # Extract trends names
   trendList = [trend['name'] for trend in trends]

   return trendList


class StreamListener(tweepy.StreamListener):
   def on_data(self, data):
      data = json.loads(data)
      try:
         #get data with no geolocation
         if data['geo'] is None:
            print('[>] {0}(@{1})\n{2}'.format(
               data['user']['name'].encode('ascii', 'ignore'),
               data['user']['screen_name'].encode('ascii', 'ignore'),
               data['text'].encode('ascii', 'ignore')
               )
         )         
         #get data with geolocation
         if data['geo'] is not None:
            print('[>] {0}(@{1}) -- LOCATION/LATITUDE/LONGITUDE: {2} / {3}'.format(
               data['user']['name'].encode('ascii', 'ignore'),
               data['user']['screen_name'].encode('ascii', 'ignore'),
               data['user']['location'].encode('ascii', 'ignore'), 
               data['geo']['coordinates']
               )
            )

         return True
      
      except Exception as e:
         print('[!] Error: {0}'.format(e))
   
   
   # On call limit
   def on_limit(self, track):
      print('[!] Limit: {0}').format(track)
      sleep(10)
   
   
   # On error stop listener
   # https://dev.twitter.com/overview/api/response-codes
   def on_error(self, status):
      print('[!] Error: {0}').format(status)
      return False


def streamAPI(auth):
   # Instantiate our listener
   l = StreamListener()
   # Instantiate the streamer with OAuth object and the listener
   streamer = tweepy.Stream(auth=auth, listener=l)
   # Define target terms for tracking
   targetTerms = ['python', 'pydata','pycones']
   # Init the streamer with terms
   streamer.filter(track=targetTerms)

   
   
def get_tag_counts(text):
   """
   Search tags in a given text. The language detection is based on stop lists.
   This implementation is inspired by https://github.com/jdf/cue.language. Thanks Jonathan Feinberg.
   """
   words = map(lambda x:x.lower(), re.findall(r'\w+', text, re.UNICODE))
   words = list(words) #** Added this
   
   s = StopWords()
   s.load_language(s.guess(words))
   
   counted = {}
   
   for word in words:
      print(word)
      if not s.is_stop_word(word) and len(word) > 1:
         if word in counted: #** if counted.has_key(word):
            counted[word] += 1
         else:
            counted[word] = 1
       #** iteritems to items
       
   return sorted(counted.items(), key=itemgetter(1), reverse=True)

try:
   api, auth = OAuth()

   print('[*] Trending topics:')
   words=[]
   # Get trending topics
   trendingTopics = getTrends(woeid=1)
   for topic in trendingTopics:
      words.append(topic.encode('ascii', 'ignore').decode('utf-8'));
      print(topic.encode('ascii', 'ignore'))
   
   print(words)
    
   text = "%s" % " ".join(words)	
      
   counts = get_tag_counts(text)
   tags = make_tags(counts, maxsize=90)
   create_tag_image(tags, 'twitter_tags.png', size=(1600, 1200))   

   print('\n[*] Initializing streamer:')
   streamAPI(auth)

except KeyboardInterrupt as e:
   exit(1)

