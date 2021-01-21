from configs import DatabaseConfig
from database.database_query import DatabaseQuery


class Database:
    def __init__(self, config: DatabaseConfig):
        pass

    def make_request(self, table_name: str) -> DatabaseQuery:
        raise NotImplementedError

