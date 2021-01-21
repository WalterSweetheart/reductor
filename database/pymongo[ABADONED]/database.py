from database import Database
from configs import DatabaseConfig
from pymongo import MongoClient
from .database_query import MongoDatabaseQuery


class MongoDatabase(Database):
    def __init__(self, config: DatabaseConfig):
        self.mongo = MongoClient("mongodb://localhost:27017/")
    
    def __del__(self):
        self.mongo.close()
    
    def make_request(self, table_name: str) -> MongoDatabaseQuery:
        return MongoDatabaseQuery(self.mongo, table_name)