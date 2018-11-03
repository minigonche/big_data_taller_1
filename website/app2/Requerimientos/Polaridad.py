#Polaridad

from django.shortcuts import render
import pymongo
import numpy as np

def hacer_requerimiento_polaridad(request, mongo_db):

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

    return render(request, 'app2/Polaridad.html', data)




def hacer_requerimiento_clasificar(request, mongo_db):

    data = {}

    polaridades = {-1:'Negativa',0:'Neutra',1:'Positiva'}
    polaridades_bg = {-1:'danger',0:'default',1:'success'}

    sexismos = {2:'Feminista Violento',1:'Feminista',0:'Neutro',-1:'Machista',-2:'Machista Violento'}
    sexismos_bg = {2:'danger',1:'warning',0:'default',-1:'primary',-2:'danger'}

    texto_entrada = request.POST.get('texto_input')
    if(texto_entrada is None or texto_entrada == ''):
        data['texto'] = ''
        data['polaridad_background'] = 'default'
        data['sexismo_background'] = 'default'
        data['polaridad'] = '---'
        data['sexismo'] = '---'
    else:
        pol = dar_polaridad(texto_entrada)
        sex = dar_polaridad(texto_entrada)

        data['texto'] = texto_entrada
        data['polaridad_background'] = polaridades_bg[pol]
        data['sexismo_background'] = sexismos_bg[sex]
        data['polaridad'] = polaridades[pol]
        data['sexismo'] = sexismos[sex]








    return render(request, 'app2/Clasificador_vivo.html', data)



def hacer_requerimiento_buscar_dsitribucion(request, mongo_db):

    data = {}

    polaridades = {-1:'Negativa',0:'Neutra',1:'Positiva'}
    polaridades_bg = {-1:'danger',0:'default',1:'success'}

    sexismos = {2:'Feminista Violento',1:'Feminista',0:'Neutro',-1:'Machista',-2:'Machista Violento'}
    sexismos_bg = {2:'danger',1:'warning',0:'default',-1:'primary',-2:'danger'}

    texto_entrada = request.POST.get('texto_input')
    if(texto_entrada is None or texto_entrada == ''):
        data['texto'] = ''
        data['polaridad_background'] = 'default'
        data['sexismo_background'] = 'default'
        data['polaridad'] = '---'
        data['sexismo'] = '---'
    else:
        pol = dar_polaridad(texto_entrada)
        sex = dar_polaridad(texto_entrada)

        data['texto'] = texto_entrada
        data['polaridad_background'] = polaridades_bg[pol]
        data['sexismo_background'] = sexismos_bg[sex]
        data['polaridad'] = polaridades[pol]
        data['sexismo'] = sexismos[sex]

    return render(request, 'app2/Distribucion.html', data)


def dar_polaridad(texto):
    #TODO
    #Hacer llamado al clasificador de verdad

    return(int(np.round(np.random.uniform()*2-1)))

def dar_sexismo(texto):
    #TODO
    #Hacer llamado al clasificador de verdad

    return(int(np.round(np.random.uniform()*2-1)))
