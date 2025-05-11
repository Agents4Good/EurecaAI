from pymongo import MongoClient

def get_mongo_collection(db_name: str, collection_name: str):
    client = MongoClient("mongodb://localhost:27017/")
    return client[db_name][collection_name]