# Script para migrar
import pymongo
import re

nombre_col = "polaridad"
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mongo_db = myclient["g7_tweets"]


words = ['colombine','feminismo']


exp = ""
for word in words:
    exp += "(?=.*" + word + "*.)"

regx = re.compile(exp, re.IGNORECASE)
conteo = mongo_db[nombre_col].aggregate([{"$match": {"full_text": regx}},{"$group": {"_id": "$polaridad", "total" : { "$sum": 1 }}} ])

for p in conteo:
    print(p)
