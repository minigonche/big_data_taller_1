from django.shortcuts import render
import tweepy
import json
import time
import requests
import base64



def hacer_requerimiento(request):

    # TODO


    return render(request, 'app3/Discusion.html', None)


def findHashtag():

    # TODO

    return

def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()     #a method from tweepy.
        except tweepy.RateLimitError:
            print('sleeping')
            time.sleep(15 * 60)
            continue

def findTweets(searchQuery, maxTweets):

    tweetsPerQry = maxTweets
    lang = "en"
    new_tweets = []

    if " " in searchQuery:
        searchQuery = searchQuery.split(' ')
        searchQuery = ''.join(searchQuery)

    searchQuery = '#' + searchQuery

    consumer_token = 'dHAWevYBB52A2W6rmROpCoOKA'
    consumer_secret = 'xKdrF5quPEkKj4GSdEaOpskjA1KUqPOGrNQpbpJqwXfONBfJJm'
    access_token = '1051945673267048448-dpEKHJPMaAmHRtWqK75Z0qBZhNkuuw'
    access_secret = 'qbyUlBhGkQS8uoVPoGOHN0DhjBWm7I5OlyNREgmnH9bg4'

    auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # If results from a specific ID onwards are reqd, set since_id to that ID.
    # else default to no lower limit, go as far back as API allows
    sinceId = None

    # If results only below a specific ID are, set max_id to that ID.
    # else default to no upper limit, start from the most recent tweet matching the search query.
    max_id = -1

    tweetCount = 0
    print("Downloading max {0} tweets".format(maxTweets))

    while tweetCount < maxTweets:
        try:
            if (max_id <= 0):
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry)
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            since_id=sinceId)
            else:
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1))
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1),
                                            since_id=sinceId)
            if not new_tweets:
                print("No more tweets found")
                break

            tweetCount += len(new_tweets)
            print("Downloaded {0} tweets".format(tweetCount))
            max_id = new_tweets[-1].id

        except tweepy.TweepError as e:
            # Just exit if any error
            print("some error : " + str(e))
            break

    tweets =[]
    for i in new_tweets:
        tweet= {}
        object = i._json
        tweet["user"] = object["user"]["screen_name"]
        tweet["text"] = object["text"]

        tweets.append(tweet)


    return tweets


def searchUsers(searchQuery, maxUsers):

    tweetsPerQry = maxUsers
    lang = "en"
    new_users = []

    consumer_token = 'dHAWevYBB52A2W6rmROpCoOKA'
    consumer_secret = 'xKdrF5quPEkKj4GSdEaOpskjA1KUqPOGrNQpbpJqwXfONBfJJm'
    access_token = '1051945673267048448-dpEKHJPMaAmHRtWqK75Z0qBZhNkuuw'
    access_secret = 'qbyUlBhGkQS8uoVPoGOHN0DhjBWm7I5OlyNREgmnH9bg4'

    auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # If results from a specific ID onwards are reqd, set since_id to that ID.
    # else default to no lower limit, go as far back as API allows
    sinceId = None

    # If results only below a specific ID are, set max_id to that ID.
    # else default to no upper limit, start from the most recent tweet matching the search query.
    max_id = -1

    tweetCount = 0
    print("Downloading max {0} tweets".format(maxUsers))

    while tweetCount < maxUsers:
        try:
            if (max_id <= 0):
                if (not sinceId):
                    new_users = api.search_users(q=searchQuery, count=tweetsPerQry)
                else:
                    new_users = api.search_users(q=searchQuery, count=tweetsPerQry,
                                            since_id=sinceId)
            else:
                if (not sinceId):
                    new_users = api.search_users(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1))
                else:
                    new_users = api.search_users(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1),
                                            since_id=sinceId)
            if not new_users:
                print("No more tweets found")
                break

            tweetCount += len(new_users)
            print("Downloaded {0} tweets".format(tweetCount))
            max_id = new_users[-1].id

        except tweepy.TweepError as e:
            # Just exit if any error
            print("some error : " + str(e))
            break

    for i in new_users:
        user = {}
        object = i._json
        user["name"] = object["name"]
        user["screen_name"] = object["screen_name"]
        user["description"] = object["description"]
        user["followers"] = object["followers_count"]
        user["img"] = object["profile_image_url"]
        user["banner"] = object["profile_banner_url"]
        return user





def makeHTML(hashtag, tweets, account):
    #  TODO

    return


def getBearer(key, secret):

    # 1. URL encode the consumer key and the consumer secret according to RFC 1738. Note that at the time of writing.
    # NOT NEEDED

    # 2. Concatenate the encoded consumer key, a colon character ”:”, and the encoded consumer secret into a single string.
    key_secret = '{}:{}'.format(key, secret).encode('ascii')

    # 3. Base64 encode the string from the previous step.
    b64_encoded_key = base64.b64encode(key_secret)
    b64_encoded_key = b64_encoded_key.decode('ascii')

    # 4. Request Bearer token.
    base_url = 'https://api.twitter.com/'
    auth_url = '{}oauth2/token'.format(base_url)

    auth_headers = {
        'Authorization': 'Basic {}'.format(b64_encoded_key),
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        }

    auth_data = {
        'grant_type': 'client_credentials'
        }

    auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)

    # 5. Request data if response ok.
    if auth_resp.status_code != 200:
        print('Invalid response {}'.format(auth_resp.status_code))
        return None

    else:
        access_token_type = auth_resp.json()['token_type']
        access_token = auth_resp.json()['access_token']

        return access_token

def findTwitterAccount(screen_name):
    #https://developer.twitter.com/en/docs/api-reference-index

    consumer_token = 'dHAWevYBB52A2W6rmROpCoOKA'
    consumer_secret = 'xKdrF5quPEkKj4GSdEaOpskjA1KUqPOGrNQpbpJqwXfONBfJJm'

    access_token = getBearer(consumer_token, consumer_secret)

    base_url = 'https://api.twitter.com/'
    search_headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }

    if " " in screen_name:
        screen_name = screen_name.split(' ')
        screen_name = ''.join(screen_name)

    search_params = {"screen_name": screen_name}

    search_url = '{}1.1/users/lookup.json'.format(base_url)

    search_resp = requests.get(search_url, headers=search_headers, params=search_params)
    search_resp = search_resp.json()
    try:
        if search_resp["errors"]:
            print(search_resp["errors"])
    except TypeError:
        if search_resp:
            object = search_resp[0]
            if object["followers_count"] > 10000:
                screen_name = object["screen_name"]
                description = object["description"]
                img = object["profile_image_url"]


                return screen_name, description, img

            else:
                return searchUsers(screen_name, 5)

    else: return searchUsers(screen_name, 5)

    return None



#response = findTweets('harry potter', 5)

response = searchUsers("alfred hitchcock", 5)
print(response)

