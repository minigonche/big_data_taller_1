import json
import pymongo
from django.shortcuts import render
from app3.Requerimientos import Preguntas as pre
from app3.Requerimientos import Entidades as ent
from app3.Requerimientos import Navegar as nav
from app3.Requerimientos.VistaEnriquecida import vista_enriquecida as ve


# Create your views here.
def index(request):
    return render(request, 'app3/index.html', None)

def Preguntas(request):

    return render(request, 'app3/Preguntas.html', None)

def search(request):
    search_query = {}
    if request.GET.get('entity_box'):  # If the form is submitted
        print("SUBMITED!")
        search_query["entidad"] = request.GET.get('entity_box', None)
        search_query["popularidad"] = request.GET.get('pop_box', None)
        search_query["user"] = request.GET.get('user_box', None)
        search_query["reputacion"] = request.GET.get('reputacion_box', None)
        print(search_query)

    return pre.hacer_requerimiento(request, search_query)

def Entidades(request):

    if (request.GET.get('search_box')):
        print('request made')
        entidad = request.GET.get('search_box', None)
        return ve.hacer_requerimiento_por_entidad(request, entidad)




def VistaEnriquecida(request):
    return ve.hacer_requerimiento(request, dar_base_de_datos())

def VistaEnriquecidaPorId(request, question_id):
    print(question_id)
    return ve.hacer_requerimiento_por_id(request, dar_base_de_datos(), question_id)

def NavegarPreguntas(request):
    return nav.hacer_requerimiento(request, dar_base_de_datos())

def getEntity(request):

    if request.method == 'GET': # If the form is submitted

        search_query = request.GET.get('search_box', None)
        print(search_query)
        url = "app3/pregunta_enriquecida/" + search_query + ".html"
        return render(request, url, search_query)

def VistaEnriquecidaPorEntidad(request, entidad):
    print(entidad)

    return ve.hacer_requerimiento_por_entidad(request, entidad)

def dar_base_de_datos():
    with open('app3/static/app3/jsons/db_configuration.json','r') as f:
        data = json.load(f)

        print("mongodb://" + data['client_location'] + "/")
        client = pymongo.MongoClient("mongodb://" + data['client_location'] + "/")
        mydb = client[data["db_name"]]

        return(mydb)

    raise("Hubo un error conectando a la base de datos")
