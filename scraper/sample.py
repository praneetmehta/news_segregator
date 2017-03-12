import sys
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

arg = sys.argv[1]
path = sys.argv[0]

Client = MongoClient() #initialize mongo client
db = Client['News']
collection = db['BBC']

news = {}
news['Page'] = int(arg)+1
try:
    collection.insert_one(news)
except:
    print 'some error'

def returner(arg, path):
	print arg, path
	return arg, path

returner(arg, path)
