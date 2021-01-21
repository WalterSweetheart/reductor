from datetime import datetime
from hashlib import sha1
from re import S
from pymongo.mongo_client import MongoClient
from database.database_query import DatabaseQuery


class MongoDatabaseQuery(DatabaseQuery):
    def __init__(self, database, table_name: str):
        self.database: MongoClient = database
        self.cluster, self.table = table_name.split(".")
        self.shard = self.database[self.cluster][self.table]
     
    #FIXME BAD CODE
    #NOTE I DID THIS BECAUSE OF MY LACK OF DATABASE PROGRAMMING AND THE LEAKING API. 

    def __BAD_CODE__get_by_user(self, username): #FIXME
        print("BADCODE get_by_user")
        return list(self.shard.find({"username": {"$eq": username}}))

    def __BAD_CODE__get_by_user_and_password(self, username, password): #FIXME
        print("BADCODE get_by_user_and_password")
        return list(self.shard.find({"username": {"$eq": username}, "password": {"$eq": password}}))
    
    def __BAD_CODE__get_by_token(self, token): #FIXME
        print("BADCODE get_by_token")
        return list(self.shard.find({"token": {"$eq": token}}))
    
    def __BAD_CODE__insert_user(self, username, password, firstname, lastname, created_at): #FIXME
        print("BADCODE insert_user")
        if len(self.__BAD_CODE__get_by_user(username)) == 0:
            self.shard.insert_one({"username": username, "password": password, "firstname": firstname, "lastname": lastname, "created_at": created_at})
        else:
            self.shard.replace_one({"username": {"$eq": username}}, {"username": username, "password": password, "firstname": firstname, "lastname": lastname, "created_at": created_at})
    
    def __BAD_CODE__insert_token(self, token, username): #FIXME
        print("BADCODE insert_token")
        if len(self.__BAD_CODE__get_by_user(username)) > 0:
            self.shard.replace_one({"username": {"$eq": username}}, {"username": username, "token": token, "created_at": datetime.now()})
        else:
            self.shard.insert_one({"username": username, "token": token, "created_at": datetime.now()})
    
    #FIXME BAD CODE
