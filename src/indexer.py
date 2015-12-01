#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 19/12/2014

@author: Martin D
'''
'''
import matplotlib.pyplot as plt
def add(a,b):
    return a+b

def addFixedValue(a):
  y = 6
  return y +a

print add(1,2)
print addFixedValue(1)
print "Hello word!!!"
plt.plot(1, 2)
plt.plot(3, 4)
plt.show()
'''
import twitter
import yaml
import json
import unicodedata
import pickle
from datetime import datetime
from elasticsearch import Elasticsearch
from json import dumps, loads, JSONEncoder, JSONDecoder
import pickle
import logging
import sys
import time
logging.basicConfig(filename='indexer.log',level=logging.INFO)

class PythonObjectEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (list, dict, str, unicode, int, float, bool, type(None))):
            return JSONEncoder.default(self, obj)
        return {'_python_object': pickle.dumps(obj)}

def as_python_object(dct):
    if '_python_object' in dct:
        return pickle.loads(str(dct['_python_object']))
    return dct


es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

consumer_key=cfg['twitter']['consumer_key']
consumer_secret=cfg['twitter']['consumer_secret']
access_token=cfg['twitter']['access_token']
access_token_secret=cfg['twitter']['access_token_secret']
username=cfg['twitter']['username']

logging.info(str(datetime.now()) + ' - Start...')
api = twitter.Api(consumer_key, consumer_secret, access_token, access_token_secret)

data = {}
max_id = None
total = 0
'''
while True:
        statuses = api.GetUserTimeline(screen_name='@subteba', count=20000, max_id=max_id)
        newCount = ignCount = 0
        for s in statuses:
            if s.id in data:
                ignCount += 1
            else:
                data[s.id] = s
                newCount += 1
        total += newCount

        if newCount == 0:
            break
        max_id = min([s.id for s in statuses]) - 1


for k in data:
    print data.get(k).text
'''
'''
friends = api.GetFriends();

for k in friends:
    print friends.get(k).name
    '''

def normalizeText(text):
    unicodedata.normalize('NFKD', text).encode('ascii','ignore')

def index(type, id, object):
    res = es.index(index="gensory", doc_type=type, id=id, body=object)
    log = 'Indexing Gensory - Type: ' + type + ' ID: ' + str(id)
    print log
    logging.debug(log)

def tweetToJSON(tweet):
    if (tweet.retweeted_status!=None):
        retweeted_status = {
                "created_at": tweet.retweeted_status.created_at,
                "favorite_count": tweet.retweeted_status.favorite_count,
                "id": tweet.retweeted_status.id,
                "lang": str(tweet.retweeted_status.lang),
                "retweet_count": tweet.retweeted_status.retweet_count,
                "text": (tweet.retweeted_status.text).encode("utf8")
              }
    else:
        retweeted_status = {}

    return {
              "created_at": tweet.created_at,
              "id": tweet.id,
              "lang": str(tweet.lang),
              "retweet_count": tweet.retweet_count,
              "retweeted_status": retweeted_status,
              "text": (tweet.text).encode("utf8"),
              "user": tweet.user.id
            }

def userToJSON(user):
    return {
                'created_at':user.created_at,
                'description':user.description,
                'favourites_count':user.favourites_count,
                'followers_count':user.followers_count,
                'friends_count':user.friends_count,
                'id':user.id,
                'lang':user.lang,
                'listed_count':user.listed_count,
                'location':user.location,
                'name':user.name,
                'profile_banner_url':user.profile_banner_url,
                'profile_image_url':user.profile_image_url,
                'screen_name':user.screen_name,
                'statuses_count':user.statuses_count,
                'url':user.url
            }

friends = api.GetFriends();
f = 0
for friend in friends:
    f+=1
    print "Iteration F#"+str(f)
    index('users', friend.id, userToJSON(friend))
    '''if (f==157):
        time.sleep(960)'''

    try:
        tweets = api.GetUserTimeline(screen_name=str(friend.screen_name), count=20000, max_id=max_id)
        for tweet in tweets:
            index('tweets', tweet.id, tweetToJSON(tweet))
    except:
        print sys.exc_info()[0]

print 'THEEND... '
logging.info(str(datetime.now()) + ' - END')