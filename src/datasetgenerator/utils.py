
def extract_type(status):
    if status['is_quote_status']:
        return 'quoted'
    elif status['retweeted']:
        return 'retweeted'
    else:
        return 'normal'


#print([s.text for s in statuses])

# To fetch a list a user's friends:
#users = api.GetFriends()
#print([u.name for u in users])

# To post a Twitter status message:
#status = api.PostUpdate('I love python-twitter!')
#print(status.text)

# To see if your credentials are successful:
#print(api.VerifyCredentials())
