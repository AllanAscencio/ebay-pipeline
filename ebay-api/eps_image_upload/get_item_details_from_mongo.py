import pymongo
import functools
import json
from bson import ObjectId  # Import ObjectId here

@functools.lru_cache(maxsize=1)
def get_mongo_client():
    return pymongo.MongoClient("mongo+uri")

@functools.lru_cache(maxsize=1)
def get_backend_database():
    client = get_mongo_client()
    return client["db-name"]

@functools.lru_cache(maxsize=1)
def get_apparel_details_table():
    db = get_backend_database()
    return db["table_name"]

def fetch_apparel_details():
    table = get_apparel_details_table()
    apparel_records = table.find({"_id": ObjectId("example_object_id")})  # Use `.find({})` for all records or add a query inside `{}`.
    return list(apparel_records)

if __name__ == "__main__":
    apparel_details = fetch_apparel_details()
    # Convert the output to a pretty-printed JSON string
    pretty_output = json.dumps(apparel_details, default=str, indent=4)
    print(pretty_output)