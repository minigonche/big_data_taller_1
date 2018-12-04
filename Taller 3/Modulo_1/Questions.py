import requests
from pymongo import MongoClient

BASEURL = "https://api.stackexchange.com/2.2/questions?"
#order=desc&sort=activity&

seguir = True #Para iterar por todas las páginas traer todos los resultados
pagina = 1

database = 'Grupo07'
MONGO_HOST= 'mongodb://bigdata-mongodb-01.virtual.uniandes.edu.co:8083/'

client = MongoClient(MONGO_HOST)

colection = client.Grupo07.Questions
#colection.drop()

inserted = 0
while seguir:
    params = {
    "site" : "movies",
    "key" : "QNg2TllXOOz9hRH9q8tj6w((",
    "pagesize" : 100,
    "filter" : "withbody",
    "page" : pagina
    }

    r = requests.get(BASEURL, params=params)
    posts = r.json()

    for post in posts['items']:
        #insertar en MongoDB
        colection.insert_one(post)
        inserted+=1
        if(inserted % 100 == 0):
            print(inserted)
            print(post)


    pagina = pagina + 1
    seguir = posts['has_more']

print(inserted)
print ("Lecturas realizadas: " + str(pagina - 1))
print ("Lecturas restantes: " + str(posts['quota_remaining']))
