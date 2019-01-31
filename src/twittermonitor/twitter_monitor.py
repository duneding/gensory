import twitter
import config
import sys
from pymongo import MongoClient

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
        collection.insert(follower._json)
        new_followers.append(follower._json)

for follower in followers_in_database:
    if not follower['id'] in current_followers:
        collection.remove({"id": follower['id']})
        unfollows.append(follower)

print('NEW FOLLOWERS:')
print('==============')
[print(new_follower['screen_name']) for new_follower in new_followers]
print()
print('UNFOLLOWERS:')
print('==============')
[print(unfollow['screen_name']) for unfollow in unfollows]





