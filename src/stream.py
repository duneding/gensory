import tweepy
import json
import config


# Authentication details. To  obtain these visit dev.twitter.com
'''
alpha = 'alpha'
beta = 'beta'
gamma = 'gamma'
zepelin = 'zepelin'
api = alpha
'''

import tweepy
import json
import sys
import engine

api = sys.argv[1]
tag = sys.argv[2]
INDEX = 'twitter'

access_token = config.value(['twitter', api, 'access_token'])
access_token_secret = config.value(['twitter', api, 'access_token_secret'])
consumer_key = config.value(['twitter', api, 'consumer_key'])
consumer_secret = config.value(['twitter', api, 'consumer_secret'])

# This is the listener, resposible for receiving data
class StdOutListener(tweepy.StreamListener):
    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)
        id = decoded['id']
        print decoded
        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        tweet = '@%s: %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore'))
        place = decoded['place']
        tweet_indexed = {
                        "favorite_count": decoded['favorite_count'],
                        "retweeted": decoded['retweeted'],                        
                        "retweet_count": decoded['retweet_count'], 
                        "in_reply_to_user_id": decoded['in_reply_to_user_id'], 
                        "favorited": decoded['favorited'],  
                        "lang": decoded['lang'],
                        "tag": tag,
                        "created_at": decoded['created_at'],
                        "text": '%s' % (decoded['text'].encode('ascii', 'ignore')),
                        "place": place
                    }        

        print tweet
        print ''
        engine.index(INDEX, 'stream', id, tweet_indexed)
        return True

    def on_error(self, status):
        print status

if __name__ == '__main__':
    l = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    print "Mostrando todos los tweets para #" + tag +":"

    # There are different kinds of streams: public stream, user stream, multi-user streams
    # In this example follow #programming tag
    # For more details refer to https://dev.twitter.com/docs/streaming-apis
    stream = tweepy.Stream(auth, l)
    stream.filter(track=[tag])



