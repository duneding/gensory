import sys
import os
import twitter
import csv
import utils
from datetime import datetime

GENSORY_PATH = os.environ.get('GENSORY_PATH')
sys.path.append(GENSORY_PATH)

import stream
import config

if (len(sys.argv) == 5):
    # alpha 50 1 margostino
    # alpha 50 0 tolkien
    app = sys.argv[1]
    limit = int(sys.argv[2])
    mode = int(sys.argv[3]) # 0:stream by #word 1:user 2:friends
    if mode == 0:
        tag = sys.argv[4]
    else:
        username = sys.argv[4]
else:
    raise Exception('Error. Parameters must be 4.')

api = twitter.Api(consumer_key = config.value(['twitter', app, 'consumer_key']),
                  consumer_secret = config.value(['twitter', app, 'consumer_secret']),
                  access_token_key = config.value(['twitter', app, 'access_token']),
                  access_token_secret = config.value(['twitter', app, 'access_token_secret']))

if mode == 0:
    results = [status._json for status in stream.get_statuses(app, tag, limit)]
elif mode == 1:
    # To fetch a single user's public status messages, where user is a Twitter user's screen name:
    results = [status._json for status in api.GetUserTimeline(screen_name=username, count=limit)]
elif mode == 2:
    results = [follower._json for follower in api.GetFollowers(screen_name=username, count=limit)]

def write_statuses(dataset_writer, statuses):
        for status in statuses:
            id = status['id']
            created_at = status['created_at']
            type = utils.extract_type(status)
            current_user_retweet = status['retweeted_status']['user']['screen_name'] if 'retweeted_status' in status else None
            favourite_count = status['favorite_count']
            favorited = status['favorited']
            #full_text = status.full_text
            geo = status['geo']
            lang = status['lang']
            place = status['place']
            possibly_sensitive = status['possibly_sensitive'] if 'possibly_sensitive' in status else None
            retweet_count = status['retweet_count']
            retweeted = status['retweeted']
            source = status['source']
            text = status['text'].replace('\n', ' ').replace(',', ' ')
            in_reply_to_user_id = status['in_reply_to_user_id']

            dataset_writer.writerow([
                id,
                created_at,
                type,
                current_user_retweet,
                favourite_count,
                favorited,
                in_reply_to_user_id,
                #full_text,
                geo,
                place,
                possibly_sensitive,
                retweet_count,
                retweeted,
                source,
                text])

for result in results:
    result['created_at'] = datetime.strptime(result['created_at'], '%a %b %d %H:%M:%S %z %Y')

with open('dataset.csv', mode='w') as dataset_file:
    dataset_writer = csv.writer(dataset_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    if mode != 2:
        write_statuses(dataset_writer, results)
    else:
        print(results[0])
