# Script para migrar
import json
import pymongo
from clasificador import Clasificador
import re



#Inicializa el clasificador

cla = Clasificador()

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["g7_tweets"]

print(myclient.list_database_names())

polaridad_count = {}
sexismo_count = {}

def actualizar_hash_clouds(texto):
    #Extrae los elementos con #
    hash_tags = re.findall(r"#(\w+)", texto)
    for hash in hash_tags:
        #Si no lo tiene lo agrega
        if(hash not in polaridad_count):
            polaridad_count[hash] = {}
            polaridad_count[hash]['polarity'] = cla.dar_polaridad(hash)
            polaridad_count[hash]['count'] = 0

            sexismo_count[hash] = {}
            sexismo_count[hash]['polarity'] = cla.dar_sexismo(hash)
            sexismo_count[hash]['count'] = 0

        #Actualiza los contadores
        polaridad_count[hash]['count'] = polaridad_count[hash]['count'] + 1
        sexismo_count[hash]['count'] = sexismo_count[hash]['count'] + 1




#Inicializa la colleccion
mydb.polaridad.drop()
mycol = mydb["polaridad"]

count = 0
with open("../scrapping/polaridad/data/2018-10-22/2018-10-22.txt",'r') as f:
    for line in f.readlines():

        item = json.loads(line)

        item['polaridad'] = cla.dar_polaridad(item['full_text'])
        item['sexismo'] = cla.dar_sexismo(item['full_text'])
        actualizar_hash_clouds(item['full_text'])
        
        count += 1
        x = mycol.insert_one(item)
        print(x.inserted_id)


print("Guardando los Word Clouds")
#Guarda los word clouds
with open("hash_cloud/frequency_polaridad.json",'w') as f:
    json.dump(polaridad_count, f)


with open("hash_cloud/frequency_sexismo.json",'w') as f:
    json.dump(sexismo_count, f)

print(count)
print("Listo")
