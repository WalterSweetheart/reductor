from configs import ApiConfig
from database import Database
from typing import Tuple


class Api:
    def __init__(self, config: ApiConfig, database: Database):
        pass

    def is_user_exists(self, username: str) -> bool:
        raise NotImplementedError

    def is_user_valid(self, username: str, password: str) -> bool:
        raise NotImplementedError

    def get_username_by_token(self, token: str) -> str:
        raise NotImplementedError
    
    def generate_user_token(self, username) -> str:
        raise NotImplementedError

    def is_token_valid(self, token: str) -> bool:
        raise NotImplementedError

    def get_user_info(self, username: str) -> dict:
        raise NotImplementedError

    def update_user_info(self, username: str, userinfo: dict) -> None:
        raise NotImplementedError

    def create_user(self, username: str, password: str, firstname: str, lastname: str) -> None:
        raise NotImplementedError

    def send_message(self, sender: str, reciever: str, message: str) -> None:
        raise NotImplementedError

    def get_user_messages(self, username: str) -> Tuple[str]:
        raise NotImplementedError
