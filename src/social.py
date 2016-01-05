__author__ = 'root'
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import twitter
import config
from textblob import TextBlob

TwitterError = twitter.TwitterError

def consumerKey(app):
    return config.value(['twitter', app, 'consumer_key'])

def consumerSecret(app):
    return config.value(['twitter', app, 'consumer_secret'])

def accessToken(app):
    return config.value(['twitter', app, 'access_token'])

def accessTokenSecret(app):
    return config.value(['twitter', app, 'access_token_secret'])

def username():
    return config.value('twitter', 'username')

def api(app):
    return twitter.Api(consumerKey(app), consumerSecret(app), accessToken(app), accessTokenSecret(app))

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

    user = {"id": tweet.user.id, "screen_name": str(tweet.user.screen_name)}

    '''
    tb_es = TextBlob(tweet.text.encode("utf-8"))
    if tb_es.detect_language() == u'es':
        text_en = tb_es.translate(to="en")
        sentiment = text_en.sentiment
    else:
        sentiment = None
    '''
    return {
              "created_at": tweet.created_at,
              "id": str(tweet.id),
              "lang": str(tweet.lang),
              "retweet_count": tweet.retweet_count,
              "retweeted_status": retweeted_status,
              "text": (tweet.text).encode("utf8"),
              "user": user#,
              #"sentiment": sentiment
            }

def userToJSON(user):

    return {
                'created_at': user.created_at,
                'description': user.description,
                'favourites_count': user.favourites_count,
                'followers_count': user.followers_count,
                'friends_count': user.friends_count,
                'id': user.id,
                'lang': user.lang,
                'listed_count': user.listed_count,
                'location': user.location,
                'name': user.name,
                #'profile_banner_url': str(user.profile_banner_url),
                'profile_image_url': user.profile_image_url,
                'screen_name': user.screen_name,
                'statuses_count': user.statuses_count,
                'url': user.url
            }

def GetTweets(api, screen_name, since_id):
        return api.GetUserTimeline(screen_name=str(screen_name), since_id=since_id, count=20000)

def GetFriends(api):
    return api.GetFriends(skip_status=True)