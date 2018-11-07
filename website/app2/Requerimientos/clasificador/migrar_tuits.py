#!/usr/bin/env python
#Script para migrar las distintas bases de datos

import random
from os import listdir
import json
import pymongo
from clasificador import Clasificador
import re
import sys
import time
import numpy as np


def actualizar_hash_clouds(texto, polaridad_count, sexismo_count, matoneo_count, cla):
    #Extrae los elementos con #
    hash_tags = re.findall(r"#(\w+)", texto)
    for hash in hash_tags:
        hash = hash.lower()
        #Si no lo tiene lo agrega
        if(hash not in polaridad_count):
            polaridad_count[hash] = {}
            polaridad_count[hash]['polarity'] = cla.dar_polaridad(hash)
            polaridad_count[hash]['count'] = 0

            sexismo_count[hash] = {}
            sexismo_count[hash]['polarity'] = cla.dar_sexismo(hash)
            sexismo_count[hash]['count'] = 0

            matoneo_count[hash] = {}
            matoneo_count[hash]['polarity'] = cla.dar_matoneo(hash)
            matoneo_count[hash]['count'] = 0


        #Actualiza los contadores
        polaridad_count[hash]['count'] = polaridad_count[hash]['count'] + 1
        sexismo_count[hash]['count'] = sexismo_count[hash]['count'] + 1
        matoneo_count[hash]['count'] = matoneo_count[hash]['count'] + 1

    return(polaridad_count, sexismo_count, matoneo_count)


def migrar(collection, numero_de_tuits, path = 'app2/Requerimientos/clasificador/tuits_todos/', guardar_hash_clouds = True):



    migrados = 0

    polaridad_count = {}
    sexismo_count = {}
    matoneo_count = {}

    cla = Clasificador()

    start_time = time.time()
    print_count = 0
    print_every = 100
    while(migrados < numero_de_tuits):
        files = listdir(path)
        random.shuffle(files)

        for file in files:
            if('.DS_Store' != file):
                with open(path + file,'r') as f:
                    print('')
                    print('Started ' + str(file))
                    print('')

                    for line in f.readlines():

                        print_count += 1
                        item = json.loads(line)

                        item['polaridad'] = cla.dar_polaridad(item['full_text'])
                        item['sexismo'] = cla.dar_sexismo(item['full_text'])
                        item['matoneo'] = cla.dar_matoneo(item['full_text'])

                        if(guardar_hash_clouds):
                            polaridad_count, sexismo_count, matoneo_count = actualizar_hash_clouds(item['full_text'], polaridad_count, sexismo_count, matoneo_count, cla)

                        migrados += 1
                        collection.insert_one(item)
                        if(print_count == print_every):
                            print_count = 0
                            print(str(migrados) + ' of ' + str(numero_de_tuits))

                        if(migrados == numero_de_tuits):

                            delta = time.time() - start_time
                            print('')
                            print('FINISHED')
                            if(delta < 60):
                                final_delta = delta
                                print('Total time: ' + str(np.round(final_delta,2)) + ' Seconds')
                            elif(delta >= 60 and delta < 3600):
                                final_delta = delta/60
                                print('Total time: ' + str(np.round(final_delta,2)) + ' Minutes')
                            else:
                                final_delta = delta/3600
                                print('Total time: ' + str(np.round(final_delta,2)) + ' Hours')

                            print('Time per Tweet: ' + str(np.round(delta/numero_de_tuits, 4)) + ' Seconds')
                            print('')

                            if(guardar_hash_clouds):
                                exportar_hash_clouds(polaridad_count, sexismo_count, matoneo_count)
                            return(True)






def exportar_hash_clouds(polaridad_count, sexismo_count, matoneo_count):

    min_count = 2

    polaridad_count_final = {}
    for key in polaridad_count.keys():
        if(polaridad_count[key]['count'] >= min_count):
            polaridad_count_final[key] = {}
            polaridad_count_final[key]['count'] = polaridad_count[key]['count']
            polaridad_count_final[key]['polarity'] = polaridad_count[key]['polarity']


    sexismo_count_final = {}
    for key in sexismo_count.keys():
        if(sexismo_count[key]['count'] >= min_count):
            sexismo_count_final[key] = {}
            sexismo_count_final[key]['count'] = sexismo_count[key]['count']
            sexismo_count_final[key]['polarity'] = sexismo_count[key]['polarity']


    matoneo_count_final = {}
    for key in matoneo_count.keys():
        if(matoneo_count[key]['count'] >= min_count):
            matoneo_count_final[key] = {}
            matoneo_count_final[key]['count'] = polaridad_count[key]['count']
            matoneo_count_final[key]['polarity'] = polaridad_count[key]['polarity']


    print('Exportando hashs')
    ubicacion = 'app2/static/app2/jsons/hash_cloud/'
    #Guarda los word clouds
    with open(ubicacion + "frequency_polaridad.json",'w') as f:
        json.dump(polaridad_count_final, f)

    with open(ubicacion + "frequency_sexismo.json",'w') as f:
        json.dump(sexismo_count_final, f)

    with open(ubicacion + "frequency_matoneo.json",'w') as f:
        json.dump(matoneo_count_final, f)



if __name__ == "__main__":

    host = 'bigdata-mongodb-01.virtual.uniandes.edu.co'
    port = 8083
    #Crear o migrar
    comando = sys.argv[1]
    #Nombre de la colleccion
    nombre_colleccion = sys.argv[2]
    #NUmero de tuits
    numero_tuits = int(sys.argv[3])


    myclient = pymongo.MongoClient("mongodb://" + host  + ':'  + str(port) + "/")
    db = myclient["Grupo07"]

    if(comando.upper() == 'CREAR'):
        if(nombre_colleccion in db.collection_names()):
            db[nombre_colleccion].drop()
            print(nombre_colleccion + ' dropped')

    collection = db[nombre_colleccion]
    migrar(collection, numero_tuits)
