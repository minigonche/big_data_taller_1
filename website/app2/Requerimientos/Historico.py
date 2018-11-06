#Historico
from django.shortcuts import render
from pymongo import MongoClient
import random
import json
from bson.code import Code
import math
import time


# client = MongoClient('localhost', 27017)
# db = client.twitterdb


# friend_collection = db.friend_collection
# collection = db.testcollection1
# ranked_collection = db.ranked_collection
# condensed_collection = db.condensed_collection
# myresults = db.myresults

def hacer_requerimiento(request, db):

    # TODO


    return render(request, 'app2/Historico.html', None)



def ranked_network(request, db):
    """
    Process the data for the webpage to use
    Export all data to the static/app2/Historico folder for D3.js to consume
    """
    friend_collection = db.friend_collection
    ranked_collection = db.ranked_collection
    condensed_collection = db.condensed_collection


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
            if count == 50:
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

def historic_growth(request, db):

    getNodes(5, 2007, db)

    return render(request, 'app2/historic_growth.html', None)

def generate_historic_collectino():


    mapper = Code("""
                function() {
                    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                    var date = this.user.created_at;
                    var user = this.user.id_str;
                    date = date.split(" ");
                    var day = String(date[2]);
                    var month = String(date[1]);
                    
                    var i;
                    for (i = 0; i < months.length; i++) {
                        if(months[i] === month){
                        month = String(i + 1);
                        }
                    }
                    
                    var year = String(date[5]);

                    emit(year.concat(month), user);
                }
                """)

    reducer = Code("""
                function(key, values) {
                    var total = 0;
                    var user_list = [];
                    var result = '';
                    for (var i = 0; i < values.length; i++) {
                        result = result.concat(values[i]).concat(',');
                    } 

                    return result
                }
                """)

    collection.map_reduce(mapper, reducer, "myresults")



def addNodes(old_user_list, new_user_list):
    for i in old_user_list:
        new_user_list.append(i)

    return new_user_list

def selectDate(month, year):
    date = str(year) + str(month)

    return date

def lastAdded(month, year, db):
    date = selectDate(month, year)
    print(date)
    result = db.myresults.find_one({"_id": date})
    user_list = result["value"]

    return user_list

def getUpUntil(month, year, db):
    myresults = db.myresults

    date = selectDate(month, year)
    print(date)
    final_list = []

    for id in myresults.find():
        users = id["value"]
        users = users[:-1]
        users_list = users.split(',')
        for i in users_list:
            if i != '':
                final_list.append(i)

        current_year = int(id["_id"][:4])
        current_month = id["_id"][-2:]
        if current_month[0] != 1:
            current_month = int(current_month[1])
        else:
            current_month= int(current_month)


        if ((year == current_year) and (month <= current_month)) or (year < current_year):
            break


    return final_list

def getNodes(month, year, db):

    condensed_collection = db.condensed_collection
    user_list = getUpUntil(month, year, db)

    sexismo = [-2, -1, 0, 1, 2]
    nodes = []
    links = []

    for user in condensed_collection.find().limit(100):
        if user["_id"] not in user_list:
            continue

        user_id = user["_id"]
        friends = user["friends"]

        # add to json
        user = {"user_id": str(user_id), "classification": sexismo[random.randint(0, 4)]}
        nodes.append(user)

        count = 0
        for friend in friends:
            if count == 50:
                break
            # add to json

            nodes.append({"user_id": str(friend), "classification": sexismo[random.randint(0, 4)]})
            link = {"source": str(user_id), "target": str(friend)}
            links.append(link)
            count += 1

    user_json = {"nodes": nodes, "links": links}

    with open(
            "/Users/andreaparra/PycharmProjects/big_data_taller_1/website/app2/static/app2/jsons/Historico/historic_data.json",
            "w") as outfile:
        json.dump(user_json, outfile)

def getDate(request, db):


    time.sleep(2)
    context = {"last_added": ''}
    response = request.POST.get('date')
    months_names = ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec','Jan', 'Feb', 'Mar']
    months_number = [4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 3]
    if response:
        year = math.floor(int(response) / 12) + 2007
        month = (int(response) - 1)%12
        month_num = months_number[month]
        month_nam = months_names[month]
        last_added = lastAdded(month_num, year, db)
        context = {"last_added": str(last_added)}

        getNodes(month_num, year, db)
        time.sleep(2)
    else:
        getNodes(4, 2007, db)




    return render(request, 'app2/historic_growth.html', context)

