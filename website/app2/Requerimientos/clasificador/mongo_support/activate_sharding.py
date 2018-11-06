
import pymongo

client = pymongo.MongoClient("mongodb://bigdata-mongodb-01.virtual.uniandes.edu.co:8083/")

print(client.admin.command('enableSharding', 'g7_tweets'))
print(client.admin.command('shardCollection', 'g7_tweets.polaridad', key={'_id': 1}))
print(client.admin.command('shardCollection', 'g7_tweets.polaridad_tiny', key={'_id': 1}))
print(client.admin.command('shardCollection', 'g7_tweets.polaridad_micro', key={'_id': 1}))
print(client.admin.command('shardCollection', 'g7_tweets.polaridad_small', key={'_id': 1}))
print(client.admin.command('shardCollection', 'g7_tweets.polaridad_medium', key={'_id': 1}))
print(client.admin.command('shardCollection', 'g7_tweets.polaridad_large', key={'_id': 1}))
print(client.admin.command('shardCollection', 'g7_tweets.polaridad_huge', key={'_id': 1}))
