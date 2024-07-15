import pymongo

class MongoDBClient:
    def __init__(self, db_name='test_db'):
        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        self.db = self.client[db_name]

    def insert_data(self, collection_name, data):
        collection = self.db[collection_name]
        collection.delete_many({})  # 清空集合中的旧数据
        collection.insert_one(data)  # 插入新数据

    def get_data(self, collection_name):
        collection = self.db[collection_name]
        return collection.find_one()
