from pymongo import MongoClient
import json
import tweepy
import time

#pymongo.collection.Collection.find()

#create a Mongoclient
client = MongoClient('localhost', 27017)

db = client.twitterdb
collection = db.testcollection1
follower_collection = db.follower_collection
friend_collection = db.friend_collection

#Tweeter developer API keys
consumer_token = 'dHAWevYBB52A2W6rmROpCoOKA'
consumer_secret = 'xKdrF5quPEkKj4GSdEaOpskjA1KUqPOGrNQpbpJqwXfONBfJJm'
access_token = '1051945673267048448-dpEKHJPMaAmHRtWqK75Z0qBZhNkuuw'
access_secret = 'qbyUlBhGkQS8uoVPoGOHN0DhjBWm7I5OlyNREgmnH9bg4'

auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)



def getHashtags():

    found = collection.find({'$and':[{'entities.hashtags.text': { '$ne': ''}}, {'entities.hashtags': { '$ne': []}}]})
    hashtag_list = []


    for i in found:
        for j in i['entities']['hashtags']:
            hashtag = j['text']
            hashtag_list.append(hashtag)

    print(hashtag_list)

def getRetweetData(more_than):
    found = collection.find({'$and': [{'retweeted_status.retweet_count': {'$gt': more_than}}, {'retweeted_status': {'$ne': ''}}]})
    count = 0
    for i in found:
        count += 1
    print(i)

def getPopular(more_than):
    found = collection.find({'user.followers_count': {'$gt': more_than}})
    count = 0
    popular = []
    for i in found:
        user = {'id': i['user']['id'], 'name': i['user']['screen_name'], 'followers': i['user']['followers_count'] }
        popular.append(user)
        count += 1
    print(count)
    print(popular)


def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()     #a method from tweepy.
        except tweepy.RateLimitError:
            print('sleeping')
            time.sleep(15 * 60)
            continue
        except tweepy.error.TweepError:
            print("Failed to run the command on that user, Skipping...")
            break

def get_followers(user_id):
    response = None
    in_collection = db.follower_collection.find_one({'_id': user_id})
    if not in_collection:
        print('User not in collection, retreiving followers')
        try:
            response = limit_handled(tweepy.Cursor(api.followers, id=user_id,count =200).pages())
        except tweepy.error.TweepError:
            print("Failed to run the command on that user, Skipping...")

    return response

def get_followers_list(response, count):
    follower_list = []
    stop = 0
    end = False
    if response:
        for page in response:
            if end:
                break
            for i in page:
                if stop == count:
                    end = True
                    break
                follower= i._json['id_str']
                follower_list.append(follower)
                stop += 1

    return follower_list

def display_results(response):
    for page in response:
        for i in page:
            print(json.dumps(i[1]._json, indent=4))


def get_network():
    found = collection.find()
    stop = 0
    follower_list = []
    for i in found:
        #if stop == 7:
            #break
        user_id = i['user']['id_str']
        print('###########{}##########'.format(user_id))
        response = get_followers(user_id)
        if response:
            follower_list = get_followers_list(response, None)
            print(follower_list)
        if follower_list != []:
            print('List generated, saving to database')
            save_adjacency_list(user_id,follower_list)
        stop += 1

def save_adjacency_list(user_id, followers):
    in_collection = db.follower_collection.find_one({'_id': user_id})

    if not in_collection:
        print('Item not in collection. Adding...')
        follower_collection.insert_one({'_id': user_id, 'followers': followers})
    else:
        print('Item already in collection. Skippping...')

def save_friend_adjacency_list(user_id, friends):
    in_collection = db.friend_collection.find_one({'_id': user_id})
    if not in_collection:
        print('Item not in collection. Adding...')
        friend_collection.insert_one({'_id': user_id, 'friends': friends})
    else:
        print('Item already in collection. Skippping...')



def get_friends(user_id):
    response = None
    in_collection = db.friend_collection.find_one({'_id': user_id})
    if not in_collection:
        print('User not in collection, retreiving friends')
        try:
            response = limit_handled(tweepy.Cursor(api.friends_ids, id=user_id, count=200).pages())
        except tweepy.error.TweepError:
            print("Failed to run the command on that user, Skipping...")

    return response

def get_friends_list(response, count):
    follower_list = []
    stop = 0
    end = False
    if response:
        for i in response:
            if end == True:
                break
            for j in i:
                if stop == count:
                    end = True
                    break
                follower_list.append(int(j))
                stop += 1

    return follower_list

def get_friend_network():
    found = collection.find()
    stop = 0
    friend_list = []
    for i in found:
        user_id = i['user']['id_str']
        print('###########{}##########'.format(user_id))
        response = get_friends(user_id)
        if response:
            friend_list = get_friends_list(response, None)
            print(friend_list)
        if friend_list != []:
            print('List generated, saving to database')
            save_friend_adjacency_list(user_id,friend_list)
        stop += 1



#getHashtags()
#getRetweetData(8000)
#getPopular(100000)
get_friend_network()
#test()
