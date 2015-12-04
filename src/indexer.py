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

LIMIT = 180
INDEX = 'gensory'
twitter_error = True

alpha = social.api('alpha')
beta = social.api('beta')
gamma = social.api('gamma')
api = alpha

#thread = list()
def worker(api, friends):

    timestamp_start = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    log_start = threading.currentThread().getName(), 'Launched'
    print log_start + ':' + timestamp_start

    """funcion que realiza el trabajo en el thread"""
    for friend in friends:
        engine.index(INDEX, 'users', friend.id, social.userToJSON(friend))

        tweets = social.GetTweets(api, friend.screen_name)

        for tweet in tweets:
            engine.index(INDEX, 'tweets', tweet.id, social.tweetToJSON(tweet))

    timestamp_end = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    log_end = threading.currentThread().getName(), 'Finishing'
    print log_end + ':' + timestamp_end
    return

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
