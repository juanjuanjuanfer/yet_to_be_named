import connection_mongo


client = connection_mongo.connect_to_mongo('-', '-')
db = client["Letterboxd"]
 
 #remove data from the collection where data doesnt contain "rating" key
collection = db["the-substance"]
collection.delete_many({"rating": {"$exists": False}})