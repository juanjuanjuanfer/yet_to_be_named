import connection_mongo


client = connection_mongo.connect_to_mongo('juan', 'lokura22')
db = client["Letterboxd"]
collection = db["reviews_the-substance"]

# get all data and store in a txt
with open('the-substance.txt', 'w', encoding='utf-8') as f:
    for doc in collection.find():
        f.write(str(doc) + '\n')