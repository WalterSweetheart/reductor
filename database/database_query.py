class DatabaseQuery:
    OP_NOT = 1
    OP_EQUALS = 2
    OP_LESS = 4
    OP_GREATER = 6

    def __init__(self, database, table_name: str):
        pass

    def filter(self, name: str, op: int, value: str) -> "DatabaseQuery":
        raise NotImplementedError

    def take(self, count: int) -> "DatabaseQuery":
        raise NotImplementedError

    def retrieve(self) -> list:
        raise NotImplementedError

    def put(self, *args):
        raise NotImplementedError

    def patch(self, **kwargs):
        raise NotImplementedError
