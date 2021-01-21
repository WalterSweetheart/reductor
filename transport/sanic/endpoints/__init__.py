from .user import UserEndpoint
from .auth import AuthEndpoint
from .msg import MsgEndpoint
from typing import Tuple
from api import Api


def get_binded_endpoints(api: Api) -> Tuple:
    return (
            UserEndpoint(api, "/user", ("GET", "POST", "PATCH")),
            AuthEndpoint(api, "/auth", ("POST", "GET",)),
            MsgEndpoint(api,  "/msg",  ("GET", "POST", "DELETE","PATCH",)),
    )
