from database.dumbdb.database_query import DumbDatabaseQuery
from database import Database, DatabaseQuery
from configs import DatabaseConfig


class DumbDatabase(Database):
    def __init__(self, config: DatabaseConfig):
        self.database = config.get_var("default_values") or dict()

    def make_request(self, table_name: str) -> DatabaseQuery:
        return DumbDatabaseQuery(self, table_name)
    