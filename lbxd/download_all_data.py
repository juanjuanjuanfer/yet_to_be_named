import connection_mongo


client = connection_mongo.connect_to_mongo('-', '-')
db = client["Letterboxd"]
source_collection = db["reviews_the-substance"]
target_collection = db["the-substance"]

# Copy all documents
documents = list(source_collection.find({}))  # Fetch all documents
if documents:
    target_collection.insert_many(documents)  # Insert them into the target collectio   n