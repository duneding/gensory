import tweepy
import json
import sys
import engine
import config
from HTMLParser import HTMLParser
from monkeylearn import MonkeyLearn


#Parametros: api_tw + tag + lang_ml + index + type
if (len(sys.argv)==6):
    api = sys.argv[1]
    tag = sys.argv[2]
    lang = sys.argv[3]
    index_es = sys.argv[4]
    type_es = sys.argv[5]
else:
    raise Exception('Error en cantidad de parametros ingresados!!!') 

access_token = config.value(['twitter', api, 'access_token'])
access_token_secret = config.value(['twitter', api, 'access_token_secret'])
consumer_key = config.value(['twitter', api, 'consumer_key'])
consumer_secret = config.value(['twitter', api, 'consumer_secret'])
    
ext = 'ext'
dune = 'dune'
api = ext
ml_token = config.value(['monkeylearn', api, lang, 'token'])
ml_module = config.value(['monkeylearn', api, lang, 'module'])

ml = MonkeyLearn(ml_token)
ml_module_id = ml_module

class StreamHTMLParser(HTMLParser):
    def handle_data(self, data):
        self.data = data

    def getData(self):
        return self.data;

parser = StreamHTMLParser()

# This is the listener, resposible for receiving data
class StdOutListener(tweepy.StreamListener):
    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)
        id = decoded['id']
        #print decoded
        parser.feed(decoded['source'])
        source = parser.getData()
        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        #tweet = '@%s: %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore'))
        tweet = decoded['text']
        place = decoded['place']
        geo = None
        if('place' in decoded):
            if (place is not None and 'bounding_box' in place):
                bounding_box=decoded['place']['bounding_box']
                geo = bounding_box['coordinates'][0][0]

        user_location = decoded['user']['location']
        sentiment = ml.classifiers.classify(ml_module_id, [tweet], sandbox=True)
        tweet_indexed = {
                        "favorite_count": decoded['favorite_count'],
                        "retweeted": decoded['retweeted'],                        
                        "retweet_count": decoded['retweet_count'], 
                        "in_reply_to_user_id": decoded['in_reply_to_user_id'], 
                        "favorited": decoded['favorited'],  
                        "lang": decoded['lang'],
                        "tag": tag,
                        "sentiment": sentiment.result[0][0],
                        "source": source,                        
                        "created_at": decoded['created_at'],
                        "text": tweet,
                        "text_not_analyzed": tweet, 
                        "place": place,
                        "geo": geo,                        
                        "user_location": user_location
                    }        

        print tweet
        print ''
        engine.index(index_es, type_es, id, tweet_indexed)
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
    while True:
        try:
            stream = tweepy.Stream(auth, l)
            stream.filter(track=[tag])
        except:
            print('Goodbye, world!')



