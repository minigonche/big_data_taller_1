from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client.twitterdb
friend_collection = db.friend_collection
collection = db.testcollection1
ranked_collection = db.ranked_collection

def getFollowerRank(tweet):

    followers = tweet["user"]["followers_count"]
    friends = tweet["user"]["friends_count"]

    followerRank = int(followers)/(int(followers) + int(friends))

    return followerRank


def getTTF(tweet):

    followers = tweet["user"]["followers_count"]
    friends = tweet["user"]["friends_count"]

    TTF = int(followers)/int(friends)

    return TTF

def main():
    for user in friend_collection.find():
        print(user["_id"])
        tweet = collection.find_one({"user.id_str": str(user["_id"])})
        TTF = getTTF(tweet)
        followerRank = getFollowerRank(tweet)
        print("TTF: {}\nFollRank: {}".format(TTF, followerRank))
        if ranked_collection.find_one({"_id": str(user["_id"])}) == None:
            item = {"_id": str(user["_id"]), "TTF": TTF, "followerRank": followerRank}
            ranked_collection.insert_one(item)





if __name__ == '__main__':
    main()