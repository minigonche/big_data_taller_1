#Polaridad

from django.shortcuts import render
import pymongo

def hacer_requerimiento(request, mongo_db):

    nombre_col = "polaridad"
    max_display = 200
    data = {}
    #Extrae los elementos tipicos

    #Polaridad
    polaridad = {'negativo':-1, 'neutro':0, 'positivo':1}
    data['polaridad'] = {}
    for pol in polaridad.keys():
        data['polaridad'][pol] = {"screen_name":"Ninguno", "full_text":"Sin Texto"}

        list = mongo_db[nombre_col].aggregate([{"$match": {"polaridad": polaridad[pol]}},{"$sample": {"size": 1}} ])

        for pos in list:
            screen_name = pos["user"]["screen_name"]
            full_text = pos["full_text"]
            if(len(full_text) > max_display):
                full_text = full_text[:max_display] + "..."

            data['polaridad'][pol] = {"screen_name":screen_name, "full_text":full_text}


    #Sexismo
    sexismo = {'machista_violento':-2, 'machista':1, 'neutro':0, 'feminista':1, "feminista_violento":2}
    data['sexismo'] = {}

    for sex in sexismo.keys():


        data['sexismo'][sex] =  {"screen_name":"Ninguno", "full_text":"Sin Texto"}
        list = mongo_db[nombre_col].aggregate([{"$match": {"sexismo": sexismo[sex]}},{"$sample": {"size": 1}} ])

        for pos in list:
            screen_name = pos["user"]["screen_name"]
            full_text = pos["full_text"]
            if(len(full_text) > max_display):
                full_text = full_text[:max_display] + "..."

            data['sexismo'][sex] = {"screen_name":screen_name, "full_text":full_text}


    print(data)
    return render(request, 'app2/Polaridad.html', data)
