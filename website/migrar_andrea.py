
import pymongo


from app2.Requerimientos.clasificador.clasificador import *

cla = Clasificador()

colleciones = ['condensed_collection','ranked_collection','testcollection1']

source_host = 'localhost'
source_port = 27017

destination_host = 'bigdata-mongodb-01.virtual.uniandes.edu.co'
destination_port = 8083

s_myclient = pymongo.MongoClient("mongodb://" + source_host  + ':'  + str(source_port) + "/")
s_db = myclient["twitterdb"]


d_client = pymongo.MongoClient("mongodb://" + destination_host  + ':'  + str(destination_port) + "/")
d_db =  myclient["Grupo07"]

for col in colleciones:

    print('started: ' + str(col))
    cursor = s_db[col].find()

    for doc in cursor:
        if(col == 'testcollection1'):
            doc['polaridad'] = cla.dar_polaridad(doc['text'])
            doc['sexismo'] = cla.dar_sexismo(doc['text'])
            doc['matoneo'] = cla.dar_matoneo(doc['text'])

        d_db[col].insert_one(doc)


print('Done')
