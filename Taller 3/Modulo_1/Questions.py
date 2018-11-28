import requests
from pymongo import MongoClient

BASEURL = "https://api.stackexchange.com/2.2/questions?"
#order=desc&sort=activity&

seguir = True #Para iterar por todas las páginas traer todos los resultados
pagina = 1
while seguir == True:
    params = {
    "site" : "movies",
    "key" : "QNg2TllXOOz9hRH9q8tj6w((",
    "pagesize" : 100,
    "filter" : "!b1MMEbcfF_H4P9",
    "page" : pagina
    }

    r = requests.get(BASEURL, params=params)
    posts = r.json()

    for post in posts['items']:
        #insertar en MongoDB
        database = 'Stack'
        coleccion = "Prueba1"
        MONGO_HOST= 'mongodb://localhost/' + database
        client = MongoClient(MONGO_HOST) 
        db = client.Stack
        db.Questions.insert(post)
    
    pagina = pagina + 1
    seguir = posts['has_more']

print ("Lecturas realizadas: " + str(pagina - 1))
print ("Lecturas restantes: " + str(posts['quota_remaining']))