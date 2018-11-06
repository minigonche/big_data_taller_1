
import pymongo

client = pymongo.MongoClient("mongodb://bigdata-mongodb-01.virtual.uniandes.edu.co:8083/")
mongo_db = client["g7_tweets"]

for col in mongo_db.collection_names():
    print('Colection : ' + str(col) + ' Size: ' + str(mongo_db[col].estimated_document_count()))
