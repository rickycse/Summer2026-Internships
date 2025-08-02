import os
import json
from datetime import datetime
from pymongo import MongoClient, UpdateOne

with open('.github/scripts/listings.json') as f:
    listings = json.load(f)

mongo_uri = os.environ["MONGO_URI"]
db_name = os.environ["MONGO_DB"]
collection_name = os.environ["MONGO_COLLECTION"]

requests = []
for job in listings:
    filter_ = {"id": job["id"]}
    job["applied"] = False
    job["date_posted_str"] = datetime.fromtimestamp(job["date_posted"]).strftime('%b %d')
    requests.append(UpdateOne(filter_, {"$set": job}, upsert=True))

client = MongoClient(mongo_uri)
db = client[db_name]
collection = db[collection_name]

if requests:
    result = collection.bulk_write(requests)
    print(f"Upserted: {result.upserted_count}, Modified: {result.modified_count}")
else:
    print("No jobs to upsert.")

print("Done syncing listings to MongoDB.")