import tweepy
import time
import json
import requests
from pymongo import MongoClient

#create a Mongoclient
client = MongoClient('localhost', 27017)

# Use twitterdb database. If it doesn't exist, it will be created.
db = client.twitterdb
collection = db.testcollection1



#Tweeter developer API keys
consumer_token = 'dHAWevYBB52A2W6rmROpCoOKA'
consumer_secret = 'xKdrF5quPEkKj4GSdEaOpskjA1KUqPOGrNQpbpJqwXfONBfJJm'
access_token = '1051945673267048448-dpEKHJPMaAmHRtWqK75Z0qBZhNkuuw'
access_secret = 'qbyUlBhGkQS8uoVPoGOHN0DhjBWm7I5OlyNREgmnH9bg4'

auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)



def get_location():
    location_access_key = 'a22fcac6e1b0c3372d259840cf9388f5'
    send_url = 'http://api.ipstack.com/190.131.240.130?access_key={}'.format(location_access_key)
    r = requests.get(send_url)
    j = json.loads(r.text)
    lat = j['latitude']
    lon = j['longitude']

    return '{},{}'.format(lat,lon)



def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()     #a method from tweepy.
        except tweepy.RateLimitError:
            print('sleeping')
            time.sleep(15 * 60)
            continue

def display_results(response):
    for page in response:
        print(json.dumps(page[1]._json, indent=4))
        break


def saveToDB(response):
    stop = 0
    for page in response:
        if stop == 10:
            break
        tweet_to_save = (dict(page[1]._json))
        collection.insert_one(tweet_to_save)

        stop =+ 1


def standardSearch(params):
    #https://developer.twitter.com/en/docs/api-reference-index
    #Este codigo actualmete requiere todos los parametros de entrada

    possible_params = ['q','lang','count', 'geocode']
    parameters_to_send = ['q','lang','count', 'geocode']
    default_params = ['required', 'en', '15', '{},100km'.format(get_location())]

    params = params.strip()
    params = params.split(',')

    for i in params:
        i = i.strip()
        key, value = i.split(':')
        if key in possible_params:
            parameters_to_send[possible_params.index(key)] = value

    for i in parameters_to_send:
        if i in possible_params:
            index = parameters_to_send.index(i)
            parameters_to_send[index] = default_params[index]

    print(parameters_to_send)


    return limit_handled(tweepy.Cursor(api.search, q=parameters_to_send[0], count=parameters_to_send[2], geocode='{}km'.format(parameters_to_send[3])).pages())


def get_followers(params):

    possible_params = ['user_id', 'count']
    parameters_to_send = ['user_id', 'count']
    default_params = ['required', '200']

    params = params.strip()
    params = params.split(',')

    for i in params:
        i = i.strip()
        key, value = i.split(':')
        if key in possible_params:
            parameters_to_send[possible_params.index(key)] = value

    for i in parameters_to_send:
        if i in possible_params:
            index = parameters_to_send.index(i)
            parameters_to_send[index] = default_params[index]

    try:
        response = limit_handled(tweepy.Cursor(api.followers, id=parameters_to_send[0],count =parameters_to_send[1]).pages())
    except tweepy.error.TweepError:
        print("Failed to run the command on that user, Skipping...")


    return response

def main():
    running = True

    #List of options
    options = ['standardSearch', 'getFollowers']

    while running == True:

        print('Which API would you like to use?:\n')
        for i in options:
            print('{}, {}'.format(i, options.index(i) + 1))
        API = input('Select one of the APIs above using their number. Type exit to quit: ')
        if API == 'exit' or API == 'quit':
            break
        if int(API) > len(options):
            print('Invalid input')
            time.sleep(2)
            continue

        print('\n')
        print('You selected {}\n'.format(options[int(API) - 1]))

        #StandardSearch
        if API == '1':

            print('These are the possible search parameters. ')
            print('q:\'query\'  -- REQUIRED\n'
                  'geocode:\'returns tweets by users within a given radius - latitude,longitude,radius (deault = your location, radius=100km)\'   -- OPTIONAL\n'
                  'lang:\'restricts tweet to given language. (Eg - es, en, fr..., default en)\' -- OPTIONAL\n'
                  'count:\'number of tweets to return per page. (Max = 100, default = 15)\'  -- OPTIONAL\n'
                  )
            correct = 'n'
            while correct == 'n':
                params = input('Input parameters as csv, with a key and value separated by a colon (:) - ')
                correct = input('These are the parameters you inputed, is this correct? {}  Y/n  '.format(params)).lower()

            #make request
            response = standardSearch(params)
            display = input('Would you like to view a sample of the retreived response?   Y/n  ')
            if display.lower() == 'y':
                display_results(response)

            save = input('Would you like to save this collection of tweets to the database?   Y/n  ')
            if save.lower() == 'y':
                saveToDB(response)

        elif API == '2':

            print('These are the possible search parameters. ')
            print('id:\'user_id to look for followers\'  -- REQUIRED\n'
                  'count:\'number of tweets to return per page. (Max = 100, default = 15)\'  -- OPTIONAL\n'
                  )
            correct = 'n'
            while correct == 'n':
                params = input('Input parameters as csv, with a key and value separated by a colon (:) - ')
                correct = input('These are the parameters you inputed, is this correct? {}  Y/n  '.format(params)).lower()


            response = get_followers(params)
            display = input('Would you like to view a sample of the retreived response?   Y/n  ')
            if display.lower() == 'y':
                display_results(response)

            save = input('Would you like to save this collection of tweets to the database?   Y/n  ')
            if save.lower() == 'y':
                saveToDB(response)

main()
print(get_location())