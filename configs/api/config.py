from datetime import timedelta


class ApiConfig:
    def __init__(self):
        self.dict = dict()
        self.dict["token_lifetime"] = timedelta(days=1)
        self.dict["userbase"] = "user_cluster.users"
        self.dict["tokenbase"] = "user_cluster.tokens"
        self.dict["messagebase"] = "message_cluster.messages"

    def get_var(self, name: str):
        if name in self.dict:
            return self.dict[name]
        return None

