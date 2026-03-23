from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


class MongoManager:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="barcelona_db", collection_name="items"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        self.collection.create_index("url", unique=True)

    def save_items(self, items):
        inserted_count = 0
        for item in items:
            try:
                self.collection.insert_one(item)
                inserted_count += 1
            except DuplicateKeyError:
                pass
        return inserted_count

    def get_all_items(self, limit=20):
        return list(self.collection.find().limit(limit))

    def get_items_by_source(self, source, limit=20):
        return list(self.collection.find({"source": source}).limit(limit))

    def count_items(self):
        return self.collection.count_documents({})