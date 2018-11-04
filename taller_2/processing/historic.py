from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client.twitterdb
friend_collection = db.friend_collection
collection = db.testcollection1

def mapper(tweet, date):

    creation_data = tweet["user"]["created_at"]
    creation_data = creation_data.strip()
    creation_data = creation_data.split(' ')
    day = int(creation_data[2])
    month = creation_data[1]
    year= int(creation_data[5])

    if year > date:
        print("returning")
        return "{}\t{}\t{}".format(day, month, year)

def main():
    for user in friend_collection.find():

        tweet = collection.find_one({"user.id_str": str(user["_id"])})
        date = mapper(tweet, 2015)
        if date:
            print(user["_id"])
            print(date)


if __name__ == '__main__':
    main()