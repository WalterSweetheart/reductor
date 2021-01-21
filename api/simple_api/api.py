from typing import NoReturn
from transport.sanic.endpoints import user
from database.database_query import DatabaseQuery
from configs import ApiConfig
from database import Database
from api import Api
from datetime import datetime, timedelta
from hashlib import md5

class SimpleApi(Api):
    def __init__(self, config: ApiConfig, database: Database):
        self.database = database
        self.config = config

    def is_user_exists(self, username: str) -> bool:
        print(username)
        return len(
            self.database.make_request(
                self.config.get_var("userbase") or "user_cluster.users"
            ).filter(
                "username", DatabaseQuery.OP_EQUALS, username
            ).take(
                1
            ).retrieve(
            )
        ) > 0

    def is_user_valid(self, username: str, password: str) -> bool:
        return len(
            self.database.make_request(
                self.config.get_var("userbase") or "user_cluster.users"
            ).filter(
                "username", DatabaseQuery.OP_EQUALS, username
            ).filter(
                "password", DatabaseQuery.OP_EQUALS, md5(password.strip().encode()).hexdigest(),
            ).take(
                1
            ).retrieve(
            )
        ) > 0

    def is_token_valid(self, token: str) -> bool:
        if len(
            data := self.database.make_request(
                self.config.get_var("tokenbase") or "user_cluster.tokens"
            ).filter(
                "token", DatabaseQuery.OP_EQUALS, token
            ).take(
                1
            ).retrieve(
            )
        ) > 0:
            print(data)
            return (data[0]["updated_at"] + self.config.get_var("token_lifetime") or timedelta(days=1)).timestamp()  > datetime.now().timestamp()
        return False

    def get_user_info(self, username: str) -> dict:
        if len(
            data := self.database.make_request(
                self.config.get_var("userbase") or "user_cluster.users"
            ).filter(
                "username", DatabaseQuery.OP_EQUALS, username
            ).take(
                1
            ).retrieve(
            )
        ) > 0:
            return data[0]
        return {}

        
    def generate_user_token(self, username: str):
        if len(
            data := self.database.make_request(
                self.config.get_var("tokenbase") or "user_cluster.tokens"
            ).filter(
                "username", DatabaseQuery.OP_EQUALS, username
            ).take(
                1
            ).retrieve(
            )
        ) > 0:
            self.database.make_request(
                self.config.get_var("tokenbase") or "user_cluster.tokens"
            ).filter(
                "username", DatabaseQuery.OP_EQUALS, username
            ).take(
                1
            ).patch(
                {
                    "updated_at": datetime.now()
                }
            )
            return self.database.make_request(
                self.config.get_var("tokenbase") or "user_cluster.tokens"
            ).filter(
                "username", DatabaseQuery.OP_EQUALS, username
            ).take(
                1
            ).retrieve(
            )[0]["token"]
        else:
            token = md5((username + str(datetime.now().microsecond)).strip().encode()).hexdigest()
            self.database.make_request(
                self.config.get_var("tokenbase") or "user_cluster.tokens"
            ).put(
                {
                    "username": username,
                    "token": token,
                    "updated_at": datetime.now(),
                }
            )
            return token

    def get_username_by_token(self, token: str) -> str:
        if len(
            data := self.database.make_request(
                self.config.get_var("tokenbase") or "user_cluster.tokens"
            ).filter(
                "token", DatabaseQuery.OP_EQUALS, token
            ).take(
                1
            ).retrieve(

            )
        ) > 0:
            return data[0]["username"]
        return ""

    def update_user_info(self, username: str, userinfo: dict) -> None:
        updatedinfo = {}
        if "password" in userinfo and userinfo["password"] is not None:
            updatedinfo["password"] = md5(userinfo["password"].strip().encode()).hexdigest()
        if "firstname" in userinfo and userinfo["firstname"] is not None:
            updatedinfo["firstname"] = userinfo["password"]
        if "lastname" in userinfo and userinfo["lastname"] is not None:
            updatedinfo["lastname"] = userinfo["lastname"]
        
        query = self.database.make_request( #YES, I can split it up
            self.config.get_var("userbase") or "user_cluster.users"
        ).filter(
            "username", DatabaseQuery.OP_EQUALS, username
        ).take(
            1
        )
        
        if len(
            query.retrieve()
        ) > 0:
            query.patch(updatedinfo)

    def create_user(self, username: str, password: str, firstname: str, lastname: str) -> None:
        if len(
            self.database.make_request(
                self.config.get_var("userbase") or "user_cluster.users"
            ).filter(
                "username", DatabaseQuery.OP_EQUALS, username
            ).take(
                1
            ).retrieve(
            )
        ) == 0:
            self.database.make_request(
                self.config.get_var("userbase") or "user_cluster.users"
            ).put(
                {
                    "username": username,
                    "password": md5(password.strip().encode()).hexdigest(),
                    "firstname": firstname,
                    "lastname": lastname,
                    "created_at": datetime.now()
                }
            )
        


    def send_message(self, sender: str, reciever: str, message: str) -> None:
        if len(
            self.database.make_request(
                self.config.get_var("userbase") or "user_cluster.users"
            ).filter(
                "username", DatabaseQuery.OP_EQUALS, sender
            ).take(
                1
            ).retrieve(
            )
        ) > 0:
            id = len(
                self.database.make_request(
                    self.config.get_var("messagebase") or "message_cluster.messages"
                ).retrieve(
                )
            )
            
            self.database.make_request(
                self.config.get_var("messagebase") or "message_cluster.messages"
            ).put(
                {
                    "id": id,
                    "sender": sender,
                    "reciever": reciever,
                    "message": message,
                    "sent_at": datetime.now(),
                }
            )

    def get_user_messages(self, username: str) -> list:
        return self.database.make_request(
            self.config.get_var("messagebase") or "message_cluster.messages"
        ).filter(
            "reciever", DatabaseQuery.OP_EQUALS, username
        ).retrieve(
        )

    def check_owner(self, username: str, id: int) -> bool:
        out = len(
            (data := self.database.make_request(
                self.config.get_var("messagebase") or "message_cluster.messages"
            ).filter(
                "id", DatabaseQuery.OP_EQUALS, id
            )).filter(
                "sender", DatabaseQuery.OP_EQUALS, username
            ).take(
                1
            ).retrieve(
            )
        ) > 0
        print(data.retrieve())
        return out

    def delete_message(self, id: int):
        self.database.make_request(
            self.config.get_var("messagebase") or "message_cluster.messages"
        ).filter(
            "id", DatabaseQuery.OP_EQUALS, id
        ).delete(
        )

    def change_message(self, id: int, message: str):
        print(
            self.database.make_request(
                self.config.get_var("messagebase") or "message_cluster.messages"
            ).filter(
                "id", DatabaseQuery.OP_EQUALS, id
            ).retrieve(
            )
        )
        self.database.make_request(
            self.config.get_var("messagebase") or "message_cluster.messages"
        ).filter(
            "id", DatabaseQuery.OP_EQUALS, id
        ).patch(
            {
                "message": message,
            }
        )
