#Historico

from django.shortcuts import render
from pymongo import MongoClient
import random
import json
import os


client = MongoClient('localhost', 27017)
db = client.twitterdb
friend_collection = db.friend_collection
collection = db.testcollection1
ranked_collection = db.ranked_collection
condensed_collection = db.condensed_collection

def hacer_requerimiento(request):

    # TODO


    return render(request, 'app2/Historico.html', None)



def ranked_network(request):
    """
    Process the data for the webpage to use
    Export all data to the static/app2/Historico folder for D3.js to consume
    """

    #os.remove("/Users/andreaparra/PycharmProjects/big_data_taller_1/website/app2/static/app2/jsons/Historico/users_test.json")
    sexismo = [-2, -1, 0, 1, 2]
    nodes = []
    links = []


    for user in condensed_collection.find().limit(100):

        user_id = user["_id"]
        friends = user["friends"]
        #add to json

        TTF = 0
        followerRank = 0

        rank_user = ranked_collection.find_one({"_id": str(user_id)})
        if rank_user != None:
            TTF = rank_user["TTF"]
            followerRank = rank_user["followerRank"]

        user = {"user_id": str(user_id), "classification": sexismo[random.randint(0,4)], "TTF": TTF, "followerRank": followerRank}
        nodes.append(user)

        count = 0
        for friend in friends:
            if count == 10:
                break
            #add to json
            TTF = 0
            followerRank = 0
            rank_user = ranked_collection.find_one({"_id": str(friend)})
            if rank_user != None:
                TTF = rank_user["TTF"]
                followerRank = rank_user["followerRank"]
            nodes.append({"user_id": str(friend), "classification": sexismo[random.randint(0,4)],"TTF": TTF, "followerRank": followerRank})
            link = {"source": str(user_id), "target": str(friend)}
            links.append(link)
            count += 1

    user_json = {"nodes": nodes, "links": links}

    with open(
        "/Users/andreaparra/PycharmProjects/big_data_taller_1/website/app2/static/app2/jsons/Historico/users_test.json",
        "w") as outfile:
        json.dump(user_json, outfile)

    return render(request, 'app2/ranked_network.html', None)

def historic_growth(request):

    # TODO

    return render(request, 'app2/historic_growth.html', None)