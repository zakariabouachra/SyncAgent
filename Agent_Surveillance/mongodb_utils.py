import api_utils
from pymongo import MongoClient

    
client = MongoClient("mongodb+srv://zackDB:2311@cluster0.uzwuxhn.mongodb.net/")
db = client["Magasin"]

def watch_collection(collection_name):
    collection = db[collection_name]
    with collection.watch() as stream:
        for change in stream:
            print(f"Reçu changement de type: {change['operationType']} dans la collection {collection_name}")

            data_payload = {
                "operation": change["operationType"],
                "data": change.get("fullDocument", {}),
                "changes": change.get("updateDescription", {}).get("updatedFields", {}),
                "database_type": "MongoDB",
                "collection_name": collection_name,
                "id":change['documentKey']['_id']
            }

            api_utils.notify_api_about_change(data_payload)
            print(data_payload)