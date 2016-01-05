#!/usr/bin/env python
# -*- coding: utf-8 -*-

import social
import engine
import sys
#import logging
import time
import threading
from datetime import datetime

#logging.basicConfig(filename='indexer.log',level=logging.INFO)

INDEX = 'gensory'
twitter_error = True

alpha = social.api('alpha')
beta = social.api('beta')
gamma = social.api('gamma')
api = alpha

#thread = list()
def worker(api, friends):

    timestamp_start = str(datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
    log_start = str((threading.currentThread().getName(), 'Launched'))
    start = log_start + ':' + timestamp_start
    print start

    for friend in friends:
        engine.index(INDEX, 'users', friend.id, social.userToJSON(friend))

        request={"size":1,"sort":[{"id":{"order":"desc"}}], "query": {"match": {
                 "user.screen_name":friend.screen_name}}}

        docs = engine.search(INDEX, 'tweets', request)
        if (len(docs["hits"]["hits"]) > 0):
            since_id = str(docs["hits"]["hits"][0][u'_id'])
        else:
            since_id = None

        tweets = social.GetTweets(api, friend.screen_name, since_id)

        for tweet in tweets:
            engine.index(INDEX, 'tweets', tweet.id, social.tweetToJSON(tweet))

    timestamp_end = str(datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
    log_end = str((threading.currentThread().getName(), 'Finishing'))
    end = log_end + ':' + timestamp_end
    print end
    return

# INDEXER

while twitter_error:
    try:
        friends = social.GetFriends(api)
        twitter_error = False
    except social.TwitterError:
        twitter_error = True
        if api == alpha:
            api = beta
        elif api == beta:
            api = gamma
        else:
            api = alpha
        print "Twitter Error:", sys.exc_info()[1]

half = len(friends)/2
alpha_thread = threading.Thread(target=worker, name='Alpha', args=(alpha, friends[:half],))
beta_thread = threading.Thread(target=worker, name='Beta', args=(beta, friends[half:],))
alpha_thread.start()
beta_thread.start()
