from pymongo import MongoClient

myClient = MongoClient("mongodb://localhost:27017")
myDatabase = myClient.iStorage
myCollection = myDatabase.iData

class Database():
    def __init__(self):
        self
    
