


import tweepy
import json
import os
from datetime import datetime
import codecs


####input your credentials here
consumer_token = 'wKx3G0hStc49NJPScB10kR9mW'
consumer_secret = 'SfOiRt05KoYn15AEEVSCMBLI6kWqkSxgRk1L3FpusVVqzizwol'
access_token = '252082539-2KC7wbROONXbo82LBg5M5sM6IbnNogfXNYSvIEZY'
access_secret = '8csBdoLM1yB9e6lcSLWDagmsJh0WkyvgSNrG3xXcGnwDo'


#Andrea
#consumer_token = 'dHAWevYBB52A2W6rmROpCoOKA'
#consumer_secret = 'xKdrF5quPEkKj4GSdEaOpskjA1KUqPOGrNQpbpJqwXfONBfJJm'
#access_token = '1051945673267048448-dpEKHJPMaAmHRtWqK75Z0qBZhNkuuw'
#access_secret = 'qbyUlBhGkQS8uoVPoGOHN0DhjBWm7I5OlyNREgmnH9bg4'


auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)
count = 100

palabras_claves = ['#IgualdadDeGenero','#machismo','#feminismo','#mujer','#hombre','#feminista','#machista','#metoo','#genero','#sexismo','#igualdad']



#revisa si ya exitse la carpeta o si no la crea
folder_name =  "data/" + datetime.now().strftime("%Y-%m-%d") + "/"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)


#Crea el nombre de los archivos
document_name =  datetime.now().strftime("%Y-%m-%d")


if not os.path.exists(folder_name + document_name + '.txt'):
    f = open(folder_name + document_name+ '.txt','w')
    f.close()


if not os.path.exists(folder_name + document_name +'.csv'):
    f = open(folder_name + document_name+ '.csv','w')
    f.write('ID,TEXTO' + "\n")
    f.close()



with open(folder_name + document_name + '.txt', 'a') as raw:
    with open(folder_name + document_name + '.csv', 'a') as csv:

        for tweet in tweepy.Cursor(api.search,q= " OR ".join(palabras_claves) + " -filter:retweets",
                                   count=count,
                                   tweet_mode='extended',
                                   #geocode="-74.08175,4.60971,100km",
                                   lang="es",
                                   since="2017-07-01").items():
            #print tweet.created_at, tweet.text, tweet.user.name, tweet.user.screen_name, tweet.retweet_count, tweet.coordinates, tweet.geo
            #print ""
            raw.write(json.dumps(tweet._json) + "\n")
            text = tweet.full_text
            text = text.replace('"',"'")
            csv.write(str(tweet.id) + ',"' + (u'' + text).encode("utf-8").strip() + '"\n')
