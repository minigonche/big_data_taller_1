from pymongo import MongoClient
import requests
import json
from nltk.corpus import stopwords
import sys
import time
import urllib.request

client = MongoClient('localhost', 27017)

db = client.TMDB
external_movie_IDs = db.external_movie_IDs

#Requiere tener la base de datos de IMDB en mongo. Para bajarla correr el metodo downloadFile(), una vez haya descargado,
#unzip y luego correr addIMDB()



def reporthook(count, block_size, total_size):
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / (1024 * duration))
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r...%d%%, %d MB, %d KB/s, %d seconds passed" %
                     (percent, progress_size / (1024 * 1024), speed, duration))
    sys.stdout.flush()


def downloadFile():
    print('Downloading movie file ...')
    url = 'https://datasets.imdbws.com/'
    filename = 'title.basics.tsv.gz'
    urllib.request.urlretrieve(url, filename, reporthook)


def addIMDB():
    f = open('title.basics.tsv', 'r')
    for line in f:
        if line[0:2] == 'tt':
            print("found movie")
            print(line)
            line = line.strip()
            titleId, tittleType, primaryTitle, originalTitle, isAdult, year, endYear, runtimeMinutes, genres = line.split(
                '\t', 8)
            external_movie_IDs.insert_one(
                {'_id': titleId, 'primaryTitle': primaryTitle, 'originalTitle': originalTitle, 'isAdult': isAdult,
                 'year': year, 'runtimeMinutes': runtimeMinutes, 'genres': genres})
            print("Movie number {} saved to DB".format(titleId[2:]))


def findInTMDB(external_ids):
    api_key = 'fb7d378d645eeef63a9cf55f052a952b'
    for ID in external_ids:
        external_id = ID["_id"]
        url = 'https://api.themoviedb.org/3/find/{}?api_key={}&external_source=imdb_id'.format(external_id, api_key)
        r = requests.get(url)
        if r.ok:
            r = json.loads(r.text)
            if r["movie_results"]:
                r = r["movie_results"][0]
                movie_object = {}
                movie_object["original_title"] = r['original_title']
                movie_object["genre_ids"] = ID["genres"]
                movie_object["runtime"] = ID["runtimeMinutes"]
                img = r["poster_path"]
                movie_object["img"] = 'https://image.tmdb.org/t/p/w500' + img
                movie_object["release_date"] = r["release_date"]
                movie_object["language"] = r["original_language"]
                movie_object["overview"] = r["overview"]
                movie_object["popularity"] = r["popularity"]

                return movie_object
    return None

def findExternalID(title):
    title = capitalize(title)
    results = []
    r = db.external_movie_IDs.find({"primaryTitle":title})
    for result in r:
        if result["runtimeMinutes"] != '\\N':
            results.append(result)


    return(results)

def capitalize(sentence):
    stop_words = set(stopwords.words('english'))
    new_sentence = ''
    sentence = sentence.split(' ')
    for word in sentence:
        if word not in stop_words:
            word = word[0:1].upper() + word[1:]
        new_sentence += ' ' + word
    new_sentence = new_sentence.strip()
    new_sentence = new_sentence[0:1].upper() + new_sentence[1:]

    return new_sentence

def findMovie(title):
    possible_ids = findExternalID(title)
    most_likely_match = findInTMDB(possible_ids)
    if most_likely_match:
        return most_likely_match
    else:
        most_likely_match = possible_ids[0]
        i = 0
        while i < len(possible_ids):
            current_match = possible_ids[i]
            if int(most_likely_match["runtimeMinutes"]) < int(current_match["runtimeMinutes"]):
                most_likely_match = current_match
            i += 1
        movie_object = {}
        movie_object["original_title"] = most_likely_match["original_title"]
        movie_object["genre_ids"] = most_likely_match["genres"]
        movie_object["runtime"] = most_likely_match["runtimeMinutes"]
        movie_object["release_date"] = most_likely_match["year"]

        return movie_object



