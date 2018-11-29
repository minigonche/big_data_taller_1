import json
import pymongo
from django.shortcuts import render
from app3.Requerimientos import Preguntas as pre
from app3.Requerimientos import Entidades as ent
from app3.Requerimientos.VistaEnriquecida import vista_enriquecida as ve


# Create your views here.
def index(request):
    return render(request, 'app3/index.html', None)

def Preguntas(request):
	return pre.hacer_requerimiento(request, dar_base_de_datos())

def Entidades(request):
	return ent.hacer_requerimiento(request, dar_base_de_datos())


def VistaEnriquecida(request):
    return ve.hacer_requerimiento(request, dar_base_de_datos())



def dar_base_de_datos():
    with open('app3/static/app3/jsons/db_configuration.json','r') as f:
        data = json.load(f)

        print("mongodb://" + data['client_location'] + "/")
        client = pymongo.MongoClient("mongodb://" + data['client_location'] + "/")
        mydb = client[data["db_name"]]

        return(mydb)

    raise("Hubo un error conectando a la base de datos")
