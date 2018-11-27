from pymongo import MongoClient
from datetime import datetime, date, timedelta
import time
import urllib.request
import gzip
import json
import sys
import os

client = MongoClient('localhost', 27017)

db = client.TMDB
movie_IDs = db.movie_IDs


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

def getToday():
    today = datetime.today().strftime('%Y-%m-%d')
    year, month, day = today.split('-', 2)

    return year, month, day

def getYesterday():
    yesterday = date.today() - timedelta(1)
    yesterday = yesterday.strftime('%Y-%m-%d')
    year, month, day = yesterday.split('-', 2)

    return year, month, day

def getDataFile(parameter):
    year, month, day = getToday()
    parameter = parameter.lower()
    print('Downloading todays {} file ...'.format(parameter))
    url = 'http://files.tmdb.org/p/exports/{}_ids_{}_{}_{}.json.gz'.format(parameter, month, day, year)
    filename = '/Users/andreaparra/Desktop/{}_ids_{}_{}_{}.json.gz'.format(parameter, month, day, year)
    urllib.request.urlretrieve(url, filename, reporthook)


def moveToDB(parameter):
    # Saves to database on _id.
    # m_123988 for movies
    # p_193874 for people
    # pc_2398 for production companies

    print('\nSaving {} file to DB'.format(parameter))

    year, month, day = getToday()

    file_path = '/Users/andreaparra/Desktop/{}_ids_{}_{}_{}.json.gz'.format(parameter, month, day, year)

    if parameter == 'movie':
        prefix = 'm_'
        name = 'original_title'
    elif parameter == 'person':
        prefix = 'p_'
        name = 'name'


    with gzip.open(file_path, 'rb') as f:
        file_content = f.read()

    file_content = file_content.decode(encoding="utf-8", errors="strict")
    file_content = file_content.strip()
    file_content = file_content.split('\n')

    for line in file_content:
        object = json.loads(line)
        id = prefix + str(object['id'])
        title = object[name]
        popularity = object['popularity']
        movie_IDs.insert_one({'_id': id, 'name': title, 'popularity': popularity})

def deleteDataFile(parameter):
    year, month, day = getToday()
    os.remove('/Users/andreaparra/Desktop/{}_ids_{}_{}_{}.json.gz'.format(parameter, month, day, year))

def main():

    files = ['movie', 'person']
    for i in files:
        try: deleteDataFile(i)
        except OSError as e: print('file not found')

        getDataFile(i)
        moveToDB(i)

main()
