# Script para migrar
import pymongo
import re
import time
import numpy as np
import random

#base de datos
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mongo_db = myclient["g7_tweets"]

#Numero de iteraciones
num_ite = 100
print_every = 10

coleccion = 'polaridad'

tamanhos = ['tiny','micro','small','medium','large']
tamanhos = ['tiny','micro','small']#,'medium','large']

pool_palabras = ['IgualdadDeGenero','machismo','feminismo','mujer','hombre','feminista','machista','metoo','genero','sexismo','igualdad']
words = ['feminismo']

random.sample([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],10)
random.randint(2,10)

final_times = {}

global_start =  time.time()

for tam in tamanhos:
    print('')
    print('Started: ' + str(tam))

    excecution_times = []
    nombre_col = coleccion + '_' + tam


    print('Size: ' + str(mongo_db[nombre_col].estimated_document_count()))


    print_count = 0
    for i in range(num_ite):

        print_count += 1
        words = random.sample(pool_palabras,random.randint(1,len(pool_palabras) - 1))

        exp = ""
        for word in words:
            exp += "(?=.*" + word + "*.)"

        regx = re.compile(exp, re.IGNORECASE)


        start_time = time.time()
        #Queries
        conteo = mongo_db[nombre_col].aggregate([{"$match": {"full_text": regx}},{"$group": {"_id": "$polaridad", "total" : { "$sum": 1 }}} ])
        final_time = time.time() - start_time
        excecution_times.append(final_time)
        if(print_count == print_every):
            print_count = 0
            print('Iteration ' + str(i+1) + ' of ' + str(num_ite) + ': ' + str(np.round(final_time,4)) + ' seconds')

    final_times[tam] = np.mean(excecution_times)

delta = time.time() - global_start

print('')
print('Finished')
if(delta < 60):
    final_delta = delta
    print('Total test time: ' + str(np.round(final_delta,2)) + ' Seconds')
elif(delta >= 60 and delta < 3600):
    final_delta = delta/60
    print('Total test time: ' + str(np.round(final_delta,2)) + ' Minutes')
else:
    final_delta = delta/3600
    print('Total test time: ' + str(np.round(final_delta,2)) + ' Hours')
print('')
print(final_times)
