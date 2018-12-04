import requests
from pymongo import MongoClient

BASEURL = "https://api.stackexchange.com/2.2/answers?filter=!3ykawN*2jyi(5ar_*"

seguir = True                           #Para iterar por todas las páginas traer todos los resultados
pagina = 1

database = 'Grupo07'
#MONGO_HOST= 'mongodb://bigdata-mongodb-01.virtual.uniandes.edu.co:8083/'
MONGO_HOST= 'localhost:27017'
client = MongoClient(MONGO_HOST)
db = client.Grupo07

colection = db.Answers

inserted = 0
while seguir:
    params = {
    "site" : "movies",
    "key" : "QNg2TllXOOz9hRH9q8tj6w((",
    "pagesize" : 100,                   #el máximo por página es 100
    #"filter" : "!3ykawN*2jyi(5ar_*",
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
