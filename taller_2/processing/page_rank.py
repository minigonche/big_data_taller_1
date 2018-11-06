import json
import numpy as np
from pymongo import MongoClient

data1 = \
[
    {"name": "A", "connections": ["B", "C"]},
    {"name": "B", "connections": ["D", "E"]},
    {"name": "D", "connections": ["A", "H"]},
    {"name": "E", "connections": ["H", "A"]},
    {"name": "H", "connections": ["A"]},
    {"name": "C", "connections": ["F", "G"]},
    {"name": "F", "connections": []},
    {"name": "G", "connections": ["A"]}
]

client = MongoClient('localhost', 27017)
db = client.twitterdb
friend_collection = db.friend_collection
condensed_collection = db.condensed_collection



def getFriends(id):

    res = condensed_collection.find_one({"_id": str(id)})
    if res != None:
        friends = res["friends"]
        return friends

def getUsers(limit):
    users_list = []
    for user in condensed_collection.find().limit(limit):
        user_id = user["_id"]
        users_list.append(user_id)

    return users_list

def getSampleData(users_list, data):
    users_to_add_empty = []
    users_to_add = []
    for user in users_list:
        friends = getFriends(user)
        friends_list = []
        count = 0
        for friend in friends:
            if count == 50:
                break
            count += 1
            if getFriends(friend) != None :
                users_to_add.append(friend)
            else:
                users_to_add_empty.append(friend)
            friends_list.append(str(friend))
        item = {"_id": str(user), "friends": friends_list}
        data.append(item)
    for user in users_to_add_empty:
        item = {"_id": str(user), "friends": []}
        data.append(item)

    if users_to_add != []:
        getSampleData(users_to_add, data)
    else:
        with open(
                "/Users/andreaparra/PycharmProjects/big_data_taller_1/taller_2/processing/real_data.json",
                "w") as outfile:
            json.dump(data, outfile)

def initializeMatrix(data):
    matrix = []
    matrix_vector = []
    n = len(data)
    for i in range(0, n):
        matrix_vector.append(data[i]["_id"])
        new = []
        for j in range(0, n):
            new.append(0)
        matrix.append(new)
    return matrix, matrix_vector

def getAdjMatrix(data):
    n = len(data)
    matrix, matrix_vector = initializeMatrix(data)
    weigth_vector = []
    print(matrix_vector)
    for i in range(n):
        weight = 0
        for j in range(n):
            if matrix_vector[j] in data[i]["friends"]:
                matrix[i][j] = 1
                weight += 1
            else: matrix[i][j] = 0
        if weight != 0:
            weigth_vector.append(1 / weight)
        else: weigth_vector.append(0)
        print(matrix[i])

    return matrix, weigth_vector

def getCosineSimilarity(v1, v2):
    similarity = np.dot(v1, v2)/(np.linalg.norm(v1) * np.linalg.norm(v2))
    return similarity

def getPageRank(adjMatrix, weight_vector, rank_vector):
    rank = True
    it = 0
    print('WEIGHTS VECTOR: {}'.format(weight_vector))

    while rank == True:
        new_rank_vector = []
        for i in range(len(adjMatrix[0])):
            summ = 0
            for j in range(len(adjMatrix)):
                summ += adjMatrix[j][i] * weight_vector[j] * rank_vector[j]
            new_rank_vector.append(summ)
        print("NEW {}".format(new_rank_vector))
        normalized = sum(new_rank_vector)

        #Normalization
        if normalized == 0:
            return None, it
        for n in range(len(new_rank_vector)):
            new_rank_vector[n] = new_rank_vector[n] / normalized
        print("NORM {}".format(new_rank_vector))
        #get cosine similarity to determine convergence
        if abs(1 - getCosineSimilarity(rank_vector, new_rank_vector)) < 0.0001:
            return new_rank_vector, it
        rank_vector = new_rank_vector

        it += 1

def main():

    users_list = getUsers(50)
    data = []
    getSampleData(users_list, data)
    print('Done getting data')

    with open('real_data.json') as f:
        data = json.load(f)

    rank = []
    for i in range(len(data)):
        rank.append(1 / len(data))

    adjMatrix, weight_vector = getAdjMatrix(data)
    rank, it = getPageRank(adjMatrix, weight_vector, rank)
    print(it, rank)


if __name__ == '__main__':
    main()

