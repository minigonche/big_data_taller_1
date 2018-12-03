

from SPARQLWrapper import SPARQLWrapper, JSON
import numpy as np

from datetime import datetime
import pandas as  pd
from io import StringIO
import random

from pymongo import MongoClient
import requests
import json
from nltk.corpus import stopwords
import sys
import time
import urllib.request


import re


client = MongoClient('localhost', 27017)

db = client.TMDB
external_movie_IDs = db.external_movie_IDs


supported_entities = ['person', 'populated place','movie']


def dar_contexto(entidad):


    #Primero saca el tipo de Entidad
    entidad = entidad.title()
    tipo = get_type_of_entity(entidad)



    #---------------------------------------------------------------
    #---------------------------------------------------------------
    #----------------------- PERSON -----------------------------
    #---------------------------------------------------------------
    #---------------------------------------------------------------
    if(tipo == 'person'):

        context = get_person_info(entidad)

        if(context['message'] != 'ok'):
            html = '''<h4> No Info Found </h4>

                        <p> No context information was found for ENTIDAD </p>

                    '''
            html = html.replace('ENTIDAD', entidad)

            return(html)


        html = '''
          <h4> Entity Context </h4>

          <p> DESCRIPCION  </p>

          <p> <strong> Age: </strong>  PERSON_AGE </p>
          <p> <strong> Gender: </strong>  PERSON_SEX </p>
          <p> <strong> Birth Place: </strong>  PERSON_BIRTH_PLACE </p>
          <p> <strong> Spouse: </strong>  PERSON_SPOUSE </p>

          <img class="d-block mx-auto mb-4" src="IMAGE_SOURCE" width="40%" alt="No Image Found" >


                  '''

        #Descripcion
        if('description' in context):
            html = html.replace('DESCRIPCION', context['description'])
        else:
            html = html.replace('DESCRIPCION', 'No description available.')


        #EDAD
        if('birth_date' in context):
            birth = datetime.strptime( context['birth_date'], "%Y-%m-%d")

            age = str( int(np.floor((datetime.now() - birth).days/365) ))

            html = html.replace('PERSON_AGE', age)
        else:
            html = html.replace('PERSON_AGE', 'No birth date available.')


        #Sexo
        if('gender' in context):
            html = html.replace('PERSON_SEX', context['gender'].title())
        else:
            html = html.replace('PERSON_SEX', 'No gender available.')

        # BIrth Place
        if('gender' in context):
            html = html.replace('PERSON_BIRTH_PLACE', context['birth_place'])
        else:
            html = html.replace('PERSON_BIRTH_PLACE', 'No birth place available.')

        #spouse
        if('spouse' in context):
            html = html.replace('PERSON_SPOUSE', context['spouse'])
        else:
            html = html.replace('PERSON_SPOUSE', 'Not Married')

        # Image
        if('img' in context and context['img'] != ''):
            img_no_param = context['img'].split('?')[0]
            html = html.replace('IMAGE_SOURCE', img_no_param)
        else:
            html = html.replace('IMAGE_SOURCE', '{% static "app3/img/person_not_found.jpg" %}')

        #Directed
        directed_movies = []
        starred_movies = []

        if('directs_movie' in context):
            movies = context['directs_movie']['movies']
            directed_movies += movies[:min(len(movies),4)]

        if('stars_movie' in context):
            movies = context['stars_movie']['movies']
            directed_movies += movies[:min(len(movies),4)]

        if(len(directed_movies) > 0 or len(starred_movies) > 0):

            extra_html = '''

                            <p> <strong> Known For: </strong> </p>
                            <div class="row">
                                <div class="col-2"></div>
                                <div class="col-8">
                                    <table class="table table-hover">
                                      <thead>
                                        <tr>
                                          <th scope="col">Stars</th>
                                          <th scope="col">Directs</th>
                                        </tr>
                                      </thead>
                                      <tbody>
                                        TABLE_ELEMENTS
                                      </tbody>
                                      </table>
                                </div>
                                <div class="col-2"></div>
                            </div>

                            <div class="py-1"><p></p></div>

                            '''
            table_elements = ''
            for i in range(max(len(directed_movies), len(starred_movies))):
                row_template = '''
                <tr>
                    <td>dir</td>
                    <td>star</td>
                </tr>
                '''
                dir = '-'
                if(i < len(directed_movies)):
                    dir = directed_movies[i]

                star = '-'
                if(i < len(starred_movies)):
                    star = starred_movies[i]

                row_template = row_template.replace('dir',dir)
                row_template = row_template.replace('star',star)

                table_elements += row_template


            extra_html = extra_html.replace('TABLE_ELEMENTS',table_elements)
            html += extra_html


        #worked with
        worked_with = []

        if('directs_movie' in context):
            actors = context['directs_movie']['actors']
            worked_with += actors


        if('stars_movie' in context):
            actors = context['stars_movie']['actors']
            worked_with += actors


        worked_with = np.unique(worked_with).tolist()

        if(len(worked_with) > 0):

            worked_with = random.sample(worked_with, min(len(worked_with),10))

            extra_html = '''

                            <p> <strong> Worked With: </strong> </p>
                            <div class="row">
                                <div class="col-2"></div>
                                <div class="col-8">
                                    <table class="table table-hover">
                                      <thead>
                                        <tr>
                                          <th scope="col">Name</th>
                                          <th scope="col">Name</th>
                                        </tr>
                                      </thead>
                                      <tbody>
                                        TABLE_ELEMENTS
                                      </tbody>
                                      </table>
                                </div>
                                <div class="col-2"></div>
                            </div>

                            <div class="py-1"><p></p></div>

                            '''

            table_elements = ''
            for i in range(int(len(worked_with)/2)):

                row_template = '''
                <tr>
                    <td>ACTOR_NAME_1</td>
                    <td>ACTOR_NAME_2</td>
                </tr>
                '''

                actor_1 = worked_with[i]
                actor_2 = worked_with[len(worked_with) - (i+1)]

                row_template = row_template.replace('ACTOR_NAME_1',actor_1)
                if(actor_1 != actor_2):
                    row_template = row_template.replace('ACTOR_NAME_2',actor_2)
                else:
                    row_template = row_template.replace('ACTOR_NAME_2', '-')

                table_elements += row_template


            extra_html = extra_html.replace('TABLE_ELEMENTS',table_elements)
            html += extra_html


    #---------------------------------------------------------------
    #---------------------------------------------------------------
    #----------------------- PLACE -----------------------------
    #---------------------------------------------------------------
    #---------------------------------------------------------------
    elif(tipo == 'populated place'):

        place = get_location_info(entidad)

        if(place['message'] != 'ok'):
            html = '''<h4> No Info Found </h4>

                        <p> No context information was found for ENTIDAD </p>

                    '''
            html = html.replace('ENTIDAD', entidad)

            return(html)

        html = '''
          <h4> Entity Context </h4>

          <p> <strong> Name: </strong>  CITY_NAME </p>

          <img class="d-block mx-auto mb-4" src="IMAGE_SOURCE" width="40%" alt="No Image Found" >

          <p> <strong> Country: </strong>  CITY_COUNTRY </p>
          <p> <strong> Area: </strong>  CITY_AREA  </p>
          <p> <strong> Population: </strong>  CITY_POPULATION </p>
          <p> <strong> Coordinates: </strong>  CITY_COORDINATES </p>

            <p> <strong> Map: </strong> </p>

             CITY_MAP


                  '''

        #replaces
        html = html.replace('CITY_NAME', entidad)
        html = html.replace('IMAGE_SOURCE', place['img'])
        html = html.replace('CITY_COUNTRY', place['country'])
        html = html.replace('CITY_AREA', place['area'])
        html = html.replace('CITY_POPULATION', place['population'])
        html = html.replace('CITY_COORDINATES', place['coordinates'])
        html = html.replace('CITY_MAP', place['google_frame'])




    #---------------------------------------------------------------
    #---------------------------------------------------------------
    #----------------------- MOVIE -----------------------------
    #---------------------------------------------------------------
    #---------------------------------------------------------------
    elif(tipo == 'movie'):


        movie = get_movie_info(entidad)

        if(movie['message'] != 'ok'):
            html = '''<h4> No Info Found </h4>

                        <p> No context information was found for ENTIDAD </p>

                    '''
            html = html.replace('ENTIDAD', entidad)

            return(html)




        html = '''
          <h4> Entity Context </h4>

          <p> <strong> Oiriginal Title: </strong>  MOVIE_TITLE </p>

          <img class="d-block mx-auto mb-4" src="IMAGE_SOURCE" width="40%" alt="No Image Found" >

          <p> <strong> Genres: </strong>  MOVIE_GENRE </p>
          <p> <strong> Runtime: </strong>  MOVIE_RUNTIME mins </p>
          <p> <strong> Release Date: </strong>  MOVIE_RELEASE_DATE </p>
          <p> <strong> Language: </strong>  MOVIE_LANGUAGE </p>
          <p> <strong> Popularity: </strong>  MOVIE_POPULARITY </p>
          <p> <strong> Plot: </strong> </p>

          <p> MOVIE_PLOT  </p>

            <p> <strong> Trailer: </strong> </p>

            <p> MOVIE_TRAILER  </p>


                  '''

        #replaces
        html = html.replace('MOVIE_TITLE', movie['original_title'])
        html = html.replace('IMAGE_SOURCE', movie['img'])
        html = html.replace('MOVIE_GENRE', movie['genre_ids'].replace(',',', '))
        html = html.replace('MOVIE_RUNTIME', movie['runtime'])
        html = html.replace('MOVIE_RELEASE_DATE', movie['release_date'])
        html = html.replace('MOVIE_LANGUAGE', movie['language'])
        html = html.replace('MOVIE_POPULARITY', str(movie['popularity']))
        html = html.replace('MOVIE_PLOT', movie['overview'])
        html = html.replace('MOVIE_TRAILER', movie['trailer_frame'])

    else:
        html = '''<h4> No Info Found </h4>

                    <p> No context information was found for ENTIDAD </p>

                '''
        html = html.replace('ENTIDAD', entidad)

    return(html)




def get_type_of_entity(search_word):

    #First the entities
    ent = [ '"' + entity + '"@en' for entity in supported_entities]

    ent_string = " ".join(ent)


    #Convert to title
    search_word = search_word.title()

    query = '''
    select ?thing_name ?label
    where {

      ?thing foaf:name "'''

    query += search_word
    query+= '''"@en.
      ?thing foaf:name ?thing_name.

      ?thing a ?entity_type.

      ?entity_type rdfs:label ?label.
      VALUES ?label {'''
    query += ent_string


    query +=  '''}.
    }
    LIMIT 1
    '''

    #print(query)
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    if(len(results["results"]["bindings"]) == 0 ):
        return('otra')

    entity = None
    for result in results["results"]["bindings"]:
        return result["label"]["value"]



def get_movie_info(movie_name):
    movie = findMovie(movie_name)
    #movie = findInTMDB(findExternalID(movie_name))
    if(movie is not None):
        movie['trailer_frame'] = get_trailer_link_frame(movie['imdb_id'])
        movie['message'] = 'ok'
    else:
        movie = {}
        movie['message'] = 'No movie found'

    return(movie)


def get_person_info(person_name):

    person_name = person_name.title()

    vars = ["name", "birth_name", "birth_date", "birth_place", "description", "gender", "img", "spouse"]
    vars_array = ['directs_movie','stars_movie']
    query = '''

            select ?name ?birth_name ?birth_date ?birth_place ?description ?gender ?img ?spouse ?directs_movie ?directs_movie_with ?directs_movie_gross ?stars_movie  ?stars_movie_with ?stars_movie_gross
            where {
              ?person foaf:name "PERSON_NAME"@en.
              ?person a foaf:Person.
             { select ?birth_date {  ?born foaf:name "PERSON_NAME"@en.
                      ?born dbo:birthDate ?birth_date.
                     } limit 1 }

              ?person dbo:birthName ?birth_name.
              ?person foaf:name ?name.

              { select ?birth_place_struct ?population { ?person dbo:birthPlace ?birth_place_struct.
                                                         ?birth_place_struct dbo:areaTotal ?population
                                                        } ORDER BY ?population limit 1 }

              ?birth_place_struct foaf:name ?birth_place.

              ?person dct:description ?description.
              ?person foaf:gender ?gender.

              OPTIONAL{?person dbo:thumbnail ?img}.


             OPTIONAL{ select ?spouse {  ?par foaf:name "PERSON_NAME"@en.
                                         ?par dbo:spouse ?spouse_struc.
                                         ?spouse_struc foaf:name ?spouse.
                      } limit 1 }

            OPTIONAL{ select ?directs_movie ?directs_movie_with ?directs_movie_gross  { ?directs_movie_struc dbo:director ?dir.
                                             ?dir foaf:name "PERSON_NAME"@en.
                                             ?directs_movie_struc dbo:gross ?directs_movie_gross.
                                             ?directs_movie_struc foaf:name ?directs_movie.

                                             ?directs_movie_struc dbo:starring ?directs_movie_with_struc.
                                             ?directs_movie_with_struc foaf:name ?directs_movie_with

                                            } ORDER BY DESC(xsd:integer(?directs_movie_gross)) }.

              OPTIONAL{ select ?stars_movie ?stars_movie_with ?stars_movie_gross  { ?starring_movie_struc dbo:starring ?star.
                                               ?star foaf:name "PERSON_NAME"@en.
                                               ?starring_movie_struc dbo:gross ?stars_movie_gross.
                                               ?starring_movie_struc foaf:name ?stars_movie.
                                               ?starring_movie_struc dbo:starring ?stars_movie_with_struc.
                                               ?stars_movie_with_struc foaf:name ?stars_movie_with
                                              } ORDER BY DESC(xsd:integer(?stars_movie_gross))  }.


            }
        '''
    query = query.replace('PERSON_NAME', person_name)

    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat('csv')
    results = sparql.query().convert()

    print(query)


    dic = {}
    text_interface = StringIO(results.decode())
    pd_result = pd.read_csv(text_interface)

    if(pd_result.shape[0] == 0 ):
        dic['message'] = 'No person under the name: ' + person_name + ' was found.'
        return(dic)

    print(pd_result.sample(3))

    dic['message'] = 'ok'
    person = pd_result.iloc[0].copy()
    person.dropna(inplace = True)

    for var in vars:
        dic[var] = ''
        if var in person.index.values:
            dic[var] = person.get(var)

    #array values
    for var in vars_array:

        dic[var] = {}
        dic[var]['movies'] = []
        dic[var]['actors'] = []
        #movies
        col = var

        temp = pd_result[[col, var + '_gross']].copy()
        temp.dropna(inplace = True)
        temp.drop_duplicates(inplace = True)

        if(temp.shape[0] > 0):

            temp.sort_values(var + '_gross', ascending = False, inplace = True)
            dic[var]['movies'] += temp[col].values.tolist()

            #actors
            col = var + '_with'

            temp = pd_result[[col, var + '_gross']].copy()
            temp.dropna(inplace = True)
            temp.drop_duplicates(inplace = True)
            temp = temp.loc[temp[col] != person_name].copy()



            temp.sort_values(var + '_gross', ascending = False, inplace = True)
            dic[var]['actors'] += temp[col].values.tolist()


    return(dic)


def get_location_info(location_name):

    fields = ["place", "area", "country", "img", "coordinates", 'population']

    location_name = location_name.title()

    query = '''

        select ?place ?area ?country ?img ?coordinates ?population
        where {
          ?place foaf:name "LOCATION_NAME"@en.
          ?place a dbo:PopulatedPlace.
          ?place dbo:areaTotal ?area.
          OPTIONAL{ select ?country{  ?city foaf:name "LOCATION_NAME"@en.
                                      ?city dbo:country ?country_struc.
                                      ?country_struc foaf:name ?country.} LIMIT 1}
          OPTIONAL{ ?place dbo:thumbnail ?img}.
          OPTIONAL{ ?place georss:point ?coordinates}.
          OPTIONAL{ ?place dbo:populationTotal ?population}.

        }
        ORDER BY DESC(?area)
        LIMIT 1

    '''

    query = query.replace('LOCATION_NAME',location_name)

    print(query)

    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    dic = {}
    if(len(results["results"]["bindings"]) == 0 ):
        dic['message'] = 'No location under the name: ' + location_name + ' was found.'
        return(dic)

    dic['message'] = 'ok'
    city = results["results"]["bindings"][0]

    for field in fields:
        if(field in city):
            dic[field] = str(city[field]['value'])
        else:
            dic[field] = 'Nothing Found'
    #iframe

    template = '<iframe src="https://www.google.com/maps/embed/v1/place?key=GOOGLE_KEY&q=LOCATION_SEARCH" allowfullscreen width="80%" height="400"></iframe>'
    location_search = location_name
    location_search = location_search.replace('  ',' ')
    location_search = location_search.replace(' ','+')
    template = template.replace('LOCATION_SEARCH', location_search)
    dic['google_frame'] = template

    return(dic)


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
        movie_object = {}

        try:
            r = requests.get(url, verify=False)

            if r.ok:
                r = json.loads(r.text)
                if r["movie_results"]:
                    r = r["movie_results"][0]

                    movie_object['imdb_id'] = external_id
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
            else: return None

        except requests.exceptions.SSLError as e:
            return None

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


def get_trailer_link_frame(imdb_id = 'tt2179136'):

    original_link = 'https://www.imdb.com/title/' + imdb_id + '/'

    fp = urllib.request.urlopen(original_link)
    mybytes = fp.read()
    page_content = mybytes.decode("utf8")
    fp.close()

    string_start = '<div class="slate">'
    string_end = "<div"

    if(string_start in page_content and string_end in page_content):

        result = page_content.split(string_start)[1]
        result = result.split(string_end)[0]

        string_start = "data-video='"
        string_end = "'"

        if(string_start in page_content and string_end in page_content):

            result = result.split(string_start)[1].split(string_end)[0]

            template = '<iframe src="https://www.imdb.com/videoembed/MOVIE_ID" allowfullscreen width="80%" height="400"></iframe>'
            template = template.replace('MOVIE_ID',result)
            return(template)


    return('No Trailer Found')



if __name__ == "__main__":

    while True:
        print('Write location name')
        print(get_location_info(input()))
