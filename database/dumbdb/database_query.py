from os import remove
from database import DatabaseQuery

class DumbDatabaseQuery(DatabaseQuery):
    def clone(self) -> "DumbDatabaseQuery":
        return DumbDatabaseQuery(self.database, self.table_name, self.result)

    def __init__(self, database, table_name: str, result: dict = None):
        self.database = database
        self.table_name = table_name
        self.result = {key: value for key, value in enumerate(database.database[table_name])} if result is None else result

    def filter(self, name: str, op: int, value: str) -> "DatabaseQuery":
        tmp = dict()
        for item in self.result.keys():
            if name not in self.result[item] or not self._get_op(op)(self.result[item][name], value):
                continue
            tmp.update({item: self.result[item]})
        self.result = tmp
        return self.clone()

    def take(self, count: int) -> "DatabaseQuery":
        tmp = dict()
        taken = 0
        for i in self.result.keys():
            print(self.result)
            tmp.update({i: self.result[i]})
            taken += 1
            if taken > count:
                break
        self.result = tmp
        return self.clone()

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

    def delete(self):
        data = {
                key: value 
                for key, value 
                in enumerate(self.database.database[self.table_name])
            }
        for key in self.result.keys():
            if key in data:
                del data[key]
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
