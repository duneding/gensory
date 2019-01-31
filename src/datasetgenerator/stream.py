import tweepy
import json
import config
from html.parser import HTMLParser

class StreamHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)

    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        print("Encountered some data  :", data)

parser = StreamHTMLParser()
statuses = None

# This is the listener, resposible for receiving data
class StdOutListener(tweepy.StreamListener):

    def __init__(self):
        super().__init__()
        self.counter = 0
        self.statuses = []

    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)
        self.statuses.append(tweepy.Status.parse(self.api, decoded))
        self.counter += 1
        return True if self.counter < self.limit else False

    def on_error(self, status):
        print(status)

def get_statuses(api, tag, limit):
    auth = tweepy.OAuthHandler(config.value(['twitter', api, 'consumer_key']), config.value(['twitter', api, 'consumer_secret']))
    auth.set_access_token(config.value(['twitter', api, 'access_token']), config.value(['twitter', api, 'access_token_secret']))
    listener = StdOutListener()
    listener.api = tweepy.API(auth)
    listener.limit = limit
    # There are different kinds of streams: public stream, user stream, multi-user streams
    # In this example follow #programming tag
    # For more details refer to https://dev.twitter.com/docs/streaming-apis
    while True:
        try:
            stream = tweepy.Stream(auth, listener)
            stream.filter(track=[tag])
            return listener.statuses
        except:
            print('Goodbye, world!')


