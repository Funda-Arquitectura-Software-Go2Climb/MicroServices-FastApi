from pymongo import MongoClient

MONGO_URL = "mongodb+srv://jerry:5kk3zt3x3BdAfB7b@fastapi.xkcvvnc.mongodb.net/?retryWrites=true&w=majority"

conn = MongoClient(MONGO_URL)