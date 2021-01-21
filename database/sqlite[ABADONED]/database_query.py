from datetime import datetime
from database import DatabaseQuery, Database
from sqlescapy import sqlescape as escape


class SqliteDatabaseQuery(DatabaseQuery):
    def __init__(self, database: Database, table_name: str):
        self.database = database
        self.table_name = table_name
        self.query = []

    def filter(self, name: str, op: int, value: str) -> DatabaseQuery:
        self.query.append({
                "type": "filter",
                "args": {
                    "name": name,
                    "op": op,
                    "value": value,
                },
            }
        )
        return self

    def take(self, count: int) -> DatabaseQuery:
        self.query.append({
                "type": "take",
                "args": {
                    "count": count,
                },
            }
        )
        return self

    def retrieve(self) -> list[dict]:
        stmt = "SELECT * FROM " + self.table_name + " "
        has_filter = False
        limit = None
        for statement in self.query:
            if statement["type"] == "filter":
                if has_filter:
                    stmt = f"SELECT * FROM ( {stmt}{'LIMIT' + str(limit) if limit is not None else ''} ) AS tmp WHERE {escape(statement['args']['name'])} {['', '!', '=', '!=', '>', '>=', '<' '<='][statement['args']['op']]} {repr(escape(statement['args']['value']))}"
                    has_filter = False
                    limit = None
                else:
                    stmt += f"WHERE {escape(statement['args']['name'])} {['', '!', '=', '!=', '>' '>=', '<', '<='][statement['args']['op']]} {repr(escape(statement['args']['value']))}"
                    has_filter = True
            if statement["type"] == "take":
                limit = int(statement["args"]["count"])
        if limit is not None:
           stmt += f" LIMIT {limit}"
        result = []
        for item in self.database.sqlite.execute(stmt):
            result.append(item)
        self.database.sqlite.commit()
        return result

    def put(self, **kwargs) -> dict:
        print(kwargs)
        stmt = f"INSERT INTO {self.table_name} ({', '.join(kwargs.keys())}) VALUES ({', '.join(map(lambda x: repr(escape(x)), kwargs.values()))})"
        print(stmt)
        self.database.sqlite.execute(stmt)
        self.database.sqlite.commit()
        return {}
    
    def patch(self, **kwargs):
        #I FUCKING HATE SQL
        # UPDATE my_relations
        # SET feelings = 'I FUCKING HATE IT'
        # WHERE thing_name = 'SQL'
        # LIMIT 1
        stmt = "SELECT * FROM " + self.table_name + " "
        has_filter = False
        limit = None
        for statement in self.query:
            if statement["type"] == "filter":
                if has_filter:
                    stmt = f"SELECT * FROM ( {stmt}{'LIMIT' + str(limit) if limit is not None else ''} ) AS tmp WHERE {escape(statement['args']['name'])} {['', '!', '=', '!=', '>', '>=', '<' '<='][statement['args']['op']]} {repr(escape(statement['args']['value']))}"
                    has_filter = False
                    limit = None
                else:
                    stmt += f"WHERE {escape(statement['args']['name'])} {['', '!', '=', '!=', '>' '>=', '<', '<='][statement['args']['op']]} {repr(escape(statement['args']['value']))}"
                    has_filter = True
            if statement["type"] == "take":
                limit = int(statement["args"]["count"])
        if limit is not None:
           stmt += f" LIMIT {limit}"
        stmt = f"UPDATE ( {stmt} ) AS tmp SET {', '.join(['%s = %s' % (key, repr(escape(value)) if isinstance(value, str) else value) for key, value in kwargs.items()])}"
        self.database.sqlite.execute(stmt)
        self.database.sqlite.commit()
        print(stmt)
