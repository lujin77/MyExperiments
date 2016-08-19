from pymongo import *

client = MongoClient(host='10.125.2.55',port=3000)
print client.database_names()
db = client.test
print db

