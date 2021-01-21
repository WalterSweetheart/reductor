from os import remove
from database import DatabaseQuery

class DumbDatabaseQuery(DatabaseQuery):
    def __init__(self, database, table_name: str):
        self.database = database
        self.table_name = table_name
        self.result = {key: value for key, value in enumerate(database.database[table_name])}

    def filter(self, name: str, op: int, value: str) -> "DatabaseQuery":
        tmp = dict()
        for item in self.result.keys():
            if name not in self.result[item] or not self._get_op(op)(self.result[item][name], value):
                continue
            tmp.update({item: self.result[item]})
        self.result = tmp
        return self

    def take(self, count: int) -> "DatabaseQuery":
        tmp = dict()
        for i in range(count + 1 if len(self.result) > count + 1 else len(self.result)):
            tmp.update({i: self.result[i]})
        self.result = tmp
        return self

    def retrieve(self) -> list:
        return list(self.result.values())

    def put(self, data: dict):
        self.database.database[self.table_name].append(data)

    def patch(self, *args):
        for i in self.result.keys():
            self.result[i].update(*args)
        data = {
                key: value 
                for key, value 
                in enumerate(self.database.database[self.table_name])
            }
        data.update(self.result)
        self.database.database[self.table_name] = [ value for _, value in data.items()]

    def _get_op(self, operator):
        return [
            None,
            None,
            lambda x, y: x == y,
            lambda x, y: x != y,
            lambda x, y: x > y,
            lambda x, y: x <= y,
            lambda x, y: x < y,
            lambda x, y: x >= y,
            ][operator]