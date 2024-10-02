from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def connect_to_mongo(username:str, password:str) -> MongoClient:
    try:
        client = f"mongodb+srv://{username}:{password}@cluster0.vajepjf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        client = MongoClient(client, server_api=ServerApi('1'))
        return client
    except Exception as e:
        print(e)
        return None