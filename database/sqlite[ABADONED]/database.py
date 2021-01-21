from database import Database, DatabaseQuery
from configs import DatabaseConfig
from .database_query import SqliteDatabaseQuery
import sqlite3 as sqlite


class SqliteDatabase(Database):
    def __init__(self, config: DatabaseConfig):
        self.sqlite = sqlite.connect(config.get_var("dbname") or "db.db")
        self.config = config
    
    def make_request(self, table_name: str) -> DatabaseQuery:
        return SqliteDatabaseQuery(self, table_name)

    def __del__(self):
        self.sqlite.close()