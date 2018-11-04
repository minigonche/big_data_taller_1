from pymongo import MongoClient

#create a Mongoclient
client = MongoClient('localhost', 27017)

db = client.twitterdb
friend_collection = db.friend_collection
condense_collection = db.condensed_collection

for check_user in friend_collection.find():
    if condense_collection.find_one({"_id": check_user["_id"]}) != None:
        print("User already in collectin, skipping")
    else:
        print("Checking user: {}".format(check_user["_id"]))
        friends = check_user["friends"]
        condensed_friends = []
        for friend in friends:
            for other_user in friend_collection.find({"_id": {"$ne": check_user["_id"]}}):
                if friend in other_user["friends"] and friend not in condensed_friends:
                    condensed_friends.append(friend)
        print(condensed_friends)
        condense_collection.insert_one({'_id': check_user["_id"], 'friends': condensed_friends})



