from django.shortcuts import render
from pymongo import MongoClient
import json

def dar_base_de_datos():
    with open('app3/static/app3/jsons/db_configuration.json','r') as f:
        data = json.load(f)

        print("mongodb://" + data['client_location'] + "/")
        client = MongoClient("mongodb://" + data['client_location'] + "/")
        mydb = client[data["db_name"]]

        return(mydb)

    raise("Hubo un error conectando a la base de datos")


def hacer_requerimiento(request, search_query):
    print(search_query)
    db = dar_base_de_datos()
    questions = []
    count = 0
    data = {}
    if search_query == {}:
        data = {"questions": '', "message": "No Questions found"}
        return render(request, 'app3/Preguntas.html', data)
    else:
        cursor = db.Questions.find(
            {"$text": {"$search": search_query["entidad"]}})
        if search_query["popularidad"]:
            popularity = int(search_query["popularidad"])
        else: popularity = ''
        user = search_query["user"]

        if popularity and user:
            for i in cursor:
                if (i["owner"]["reputation"] > popularity) and (i["owner"]["display_name"] == user):
                    questions.append(i)
                if count == 10:
                    break
                count += 1

        elif popularity :
            for i in cursor:
                if (i["owner"]["reputation"] > popularity):
                    questions.append(i)
                if count == 10:
                    break
                count += 1

        elif user:
            for i in cursor:
                if (i["owner"]["display_name"] == user):
                    questions.append(i)
                if count == 10:
                    break
                count += 1

        else:
            for i in cursor:
                questions.append(i)
                if count == 10:
                    break
                count += 1

        data['questions'] = questions

        print(data)

        return render(request, 'app3/search_results.html', data)

