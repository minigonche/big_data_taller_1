#Historico

from django.shortcuts import render
from pymongo import MongoClient
import random
import json
import os


client = MongoClient('localhost', 27017)
db = client.twitterdb
friend_collection = db.friend_collection

def hacer_requerimiento(request):

    # TODO

    process_data()
    return render(request, 'app2/Historico.html', None)


def process_data():
    """
    Process the data for the webpage to use
    Export all data to the static/app2/Historico folder for D3.js to consume
    """

    os.remove("/Users/andreaparra/PycharmProjects/big_data_taller_1/website/app2/static/app2/jsons/Historico/users_test.json")
    sexismo = [-2, -1, 0, 1, 2]
    nodes = []
    links = []


    for user in friend_collection.find().limit(50):

        user_id = user["_id"]
        friends = user["friends"]
        #add to json
        user = {"user_id": str(user_id), "classification": sexismo[random.randint(0,4)]}
        nodes.append(user)

        count = 0
        for friend in friends:
            if count == 50:
                break
            #add to json
            nodes.append({"user_id": str(friend), "classification": sexismo[random.randint(0,4)]})
            link = {"source": str(user_id), "target": str(friend)}
            links.append(link)
            count += 1

    user_json = {"nodes": nodes, "links": links}

    with open(
        "/Users/andreaparra/PycharmProjects/big_data_taller_1/website/app2/static/app2/jsons/Historico/users_test.json",
        "w") as outfile:
        json.dump(user_json, outfile)

