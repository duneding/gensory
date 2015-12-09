'''
Created on 19/12/2014

@author: Martin D
'''
from __future__ import absolute_import, print_function

import tweepy
import random
# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
consumer_key="inFi4vua1u4qK8D2QWQv7EDCI"
consumer_secret="m1JJ2Uph2x1XyVs4fImNQt2LbmfwWs56wYkBoi0LPYdHkpywdw"

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located
# under "Your access token")
access_token="49469747-y6lqBn2tETPyzTgMxDKVDavzTTTRgwgY7CcUXHZJh"
access_token_secret="zxlRIAFFzuaXPcQk6gUvgRncdps5nqJxp51pcoRnkMyf9"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.secure = True
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# If the authentication was successful, you should
# see the name of the account print out
print(api.me().name)

follow2 = api.followers_ids()  
print(len(follow2))  

show_list = str(raw_input("Do you want to list the followers array?"))  
if show_list == ('y' or 'yes' or 'Y' or 'Yes' or 'YES'):  
    print(follow2)  
  
def pick_winner():  
    random_number = random.randint(0, len(follow2)-1)  
    winner = api.get_user(follow2[random_number])  
    print(winner.screen_name, random_number)  
  
while True:  
    pick = raw_input("Press Enter to pick a winner, Q to quit.")  
    if pick == ('q' or 'Q' or 'quit' or 'QUIT' or 'Quit'):  
        break  
    pick_winner() 
    
for status in tweepy.Cursor(api.user_timeline).items():
    for tweet in tweepy.Cursor(api.search,
                               q="google",
                               rpp=100,
                               result_type="recent",
                               include_entities=True,
                               lang="en").items():
        print(tweet.created_at, tweet.text)    
        
# If the application settings are set for "Read and Write" then
# this line should tweet out the message to your account's
# timeline. The "Read and Write" setting is on https://dev.twitter.com/apps
#api.update_status('Updating using OAuth authentication via Tweepy!')