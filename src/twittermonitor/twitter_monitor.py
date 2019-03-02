def load_src(name, fpath):
    import os, importlib
    return importlib.util.find_spec(name, os.path.join(os.path.dirname(__file__), fpath))

#load_src("config", "../config.py")
import os, sys
#first change the cwd to the script path
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
os.chdir(scriptPath)

#append the relative location you want to import from
sys.path.append("../")

import twitter
import config
import sys
from pymongo import MongoClient
import datetime

client = MongoClient('localhost', 27017)
db = client.local
collection = db.twitter_monitor

if (len(sys.argv) == 3):
    app = sys.argv[1]
    username = sys.argv[2]
else:
    raise Exception('Error. Parameters must be 3.')

api = twitter.Api(consumer_key = config.value(['twitter', app, 'consumer_key']),
                  consumer_secret = config.value(['twitter', app, 'consumer_secret']),
                  access_token_key = config.value(['twitter', app, 'access_token']),
                  access_token_secret = config.value(['twitter', app, 'access_token_secret']))

followers_in_twitter = api.GetFollowers(screen_name='margostino')
followers_in_database = collection.find()

new_followers = []
unfollows = []
current_followers = []

for follower in followers_in_twitter:
    exists = collection.find_one({"id": follower.id}) != None
    current_followers.append(follower.id)
    if not exists:
        follower._json['follower_since'] = f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}"
        collection.insert(follower._json)
        new_followers.append(follower._json)

for follower in followers_in_database:
    if not follower['id'] in current_followers:
        collection.remove({"id": follower['id']})
        unfollows.append(follower)

print('TOTAL:')
print('======')
print(len(current_followers))
print()
print('NEW FOLLOWERS:')
print('==============')
print()
[print(new_follower['screen_name']) for new_follower in new_followers]
print()
print('UNFOLLOWERS:')
print('==============')
[print((unfollow['screen_name'] + '- Since ' + unfollow['follower_since'] if 'follower_since' in unfollow else '')) for unfollow in unfollows]
print()
