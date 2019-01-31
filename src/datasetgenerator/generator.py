import twitter
import csv
import config
import sys
import utils
import stream
from datetime import datetime

if (len(sys.argv) == 5):
    app = sys.argv[1]
    limit = int(sys.argv[2])
    mode = int(sys.argv[3]) # 0:stream 1:user

    if mode == 1:
        username = sys.argv[4]
    elif mode == 0:
        tag = sys.argv[4]
else:
    raise Exception('Error. Parameters must be 4.')

if mode == 1:
    api = twitter.Api(consumer_key = config.value(['twitter', app, 'consumer_key']),
                      consumer_secret = config.value(['twitter', app, 'consumer_secret']),
                      access_token_key = config.value(['twitter', app, 'access_token']),
                      access_token_secret = config.value(['twitter', app, 'access_token_secret']))
    # To fetch a single user's public status messages, where user is a Twitter user's screen name:
    statuses = [status._json for status in api.GetUserTimeline(screen_name='margostino', count=limit)]
elif mode == 0:
    statuses = [status._json for status in stream.get_statuses(app, tag, limit)]

for status in statuses:
    status['created_at'] = datetime.strptime(status['created_at'], '%a %b %d %H:%M:%S %z %Y')

with open('dataset.csv', mode='w') as dataset_file:
    dataset_writer = csv.writer(dataset_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

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

