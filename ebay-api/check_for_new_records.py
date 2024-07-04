import time
from pymongo import MongoClient

MONGO_URI = 'mongo+uri'
DB_NAME = 'backend_database'
COLLECTION_NAME = 'collection_name'

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def check_new_records():
    last_checked = time.time()
    while True:
        current_time = time.time()
        new_records = collection.find({"created_at": {"$gt": last_checked}})
        for record in new_records:
            print("New record found:", record)
        last_checked = current_time
        time.sleep(10)  # Check every 10 seconds

if __name__ == "__main__":
    check_new_records()
