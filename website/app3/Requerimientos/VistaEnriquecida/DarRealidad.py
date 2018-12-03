import tweepy
import time

def dar_realidad(entidad):

    twitterAccount = findTwitterAccount(entidad)
    tweets = findTweets(entidad)

    if(twitterAccount and tweets):

        html = '''
            <h4> Entity Reality </h4>
            <h5> Cuenta de twitter mas relevante relacionadad con <b>NAME</b>: <i>@SCREEN</i> </h5>
            <p> DESCRIPCION </p>

            <img class="d-block mx-auto mb-4" src="SRC" width="20%"  alt="" >

            <p> COM_1 </p>
            

                  '''
        html = html.replace('SRC', twitterAccount["img"])
        html = html.replace('NAME', twitterAccount["name"])
        html = html.replace('DESCRIPCION', twitterAccount["description"])
        html = html.replace('SCREEN', twitterAccount["screen_name"])

        i = 0
        comentarios = ''
        while i < len(tweets):
            comentarios = comentarios + "<p>" + tweets[i]["text"] + "</p>"
            i += 1

        html = html.replace('COM_1', comentarios)



    else:
        html = '''<h4> No Info Found </h4>

                    <p> No reality information was found for ENTIDAD </p>

                '''
        html = html.replace('ENTIDAD', entidad)

    return(html)

def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()     #a method from tweepy.
        except tweepy.RateLimitError:
            print('sleeping')
            time.sleep(15 * 60)
            continue


def findTweets(searchQuery):

    maxTweets = 5
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

def findTwitterAccount(searchQuery):

    maxUsers = 5
    tweetsPerQry = maxUsers
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
    print("Downloading max {0} accounts".format(maxUsers))

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
                print("No more accounts found")
                break

            tweetCount += len(new_users)
            print("Downloaded {0} accounts".format(tweetCount))
            max_id = new_users[-1].id

        except tweepy.TweepError as e:
            # Just exit if any error
            print("some error : " + str(e))
            break

    for i in new_users:
        user = {}
        object = i._json
        try:
            user["name"] = object["name"]
        except KeyError:
            user["name"] = ''
            print("no item found")
        try:
            user["screen_name"] = object["screen_name"]
        except KeyError:
            user["screen_name"] = ''
            print("no item found")
        try:
            user["description"] = object["description"]
        except KeyError:
            user["description"] = ''
            print("no item found")
        try:
            user["followers"] = object["followers_count"]
        except KeyError:
            user["followers"] = ''
            print("no item found")
        try:
            user["img"] = object["profile_image_url"]
        except KeyError:
            user["img"] = ''
            print("no item found")
        try:
            user["banner"] = object["profile_banner_url"]
        except KeyError:
            user["banner"] = ''
            print("no item found")

        return user


print(findTweets("American Sniper"))