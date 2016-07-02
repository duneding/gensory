#!/usr/bin/env python
# -*- coding: utf-8 -*-

import social
import engine
import config
import sys
#import logging
import time
import threading
from datetime import datetime

#Parametros: api_tw
#Ej: python src/scrapy.py alpha

#logging.basicConfig(filename='indexer.log',level=logging.INFO)

INDEX = 'scrapy'

accounts = config.value(['twitter','accounts'])

timestamp_start = str(datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
start = 'Start: ' + timestamp_start
print start

if (len(sys.argv)==2):
    api_param = sys.argv[1]
else:
    raise Exception('Error en cantidad de parametros ingresados!!!')

api = social.api(api_param)

for account in accounts:
    print 'Indexing ' + account
    user = social.GetUser(api,account)
    id = user.__getattribute__('_id')
    engine.index(INDEX, 'user', id, social.userToJSON(user))

    request={"size":1,"sort":[{"id":{"order":"desc"}}], "query": {"match": {
                 "user.screen_name":account}}}

    docs = engine.search(INDEX, 'tweet', request)
    if (len(docs["hits"]["hits"]) > 0):
        since_id = str(docs["hits"]["hits"][0][u'_id'])
    else:
        since_id = None

    tweets = social.GetTweets(api, account, since_id)

    for tweet in tweets:
        print 'Tweet>  ' + tweet.text
        engine.index(INDEX, 'tweet', tweet.id, social.tweetToJSON(tweet))
