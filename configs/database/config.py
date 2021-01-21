class DatabaseConfig:
    def __init__(self):
        self.dict = dict()
        self.dict["default_values"] = {
            "user_cluster.users": list(),
            "user_cluster.tokens": list(),
            "message_cluster.messages": list(),
        }

    def get_var(self, key):
        if key in self.dict:
            return self.dict[key]
        return None
