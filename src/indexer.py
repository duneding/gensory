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
import unicodedata
import logging
from datetime import datetime
from elasticsearch import Elasticsearch

logging.basicConfig(filename='indexer.log',level=logging.INFO)

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

ck_alfa=cfg['twitter']['alfa']['consumer_key']
cs_alfa=cfg['twitter']['alfa']['consumer_secret']
at_alfa=cfg['twitter']['alfa']['access_token']
ats_alfa=cfg['twitter']['alfa']['access_token_secret']

ck_beta=cfg['twitter']['beta']['consumer_key']
cs_beta=cfg['twitter']['beta']['consumer_secret']
at_beta=cfg['twitter']['beta']['access_token']
ats_beta=cfg['twitter']['beta']['access_token_secret']

username=cfg['twitter']['username']

logging.info(str(datetime.now()) + ' - Start...')
alfa = twitter.Api(ck_alfa, cs_alfa, at_alfa, ats_alfa)
beta = twitter.Api(ck_beta, cs_beta, at_beta, ats_beta)

data = {}
total = 0

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

def getAndIndexTweets(api, screen_name):
        max_id = None
        tweets = api.GetUserTimeline(screen_name=str(friend.screen_name), count=20000, max_id=max_id)
        for tweet in tweets:
            index('tweets', tweet.id, tweetToJSON(tweet))

friends = alfa.GetFriends();
f = 0
LIMIT = 180
for friend in friends:
    f+=1
    print "Iteration F#"+str(f)
    index('users', friend.id, userToJSON(friend))

    if (f<=LIMIT):
        getAndIndexTweets(alfa, friend.screen_name)
    else:
        getAndIndexTweets(beta, friend.screen_name)

print 'THEEND: ' + str(f);