from transport.sanic.endpoint_base import EndpointBase
from sanic.request import Request
from sanic.response import BaseHTTPResponse, json


class UserEndpoint(EndpointBase):
    async def method_get(self, request: Request, body: dict) -> BaseHTTPResponse:
        if "token" not in request.cookies:
            return json({"Status": "Fail. Autorization is required"})
        if not self.api.is_token_valid(request.cookies["token"]):
            return json({"Status": "Fail. Token is invalid. Please, relogin"})

        userinfo = self.api.get_user_info(self.api.get_username_by_token(request.cookies["token"]))
        return json({"username": userinfo["username"], "firstname": userinfo["firstname"], "created_at": str(userinfo["created_at"])})

    async def method_post(self, request: Request, body: dict) -> BaseHTTPResponse:
        data = body["DATA"]
        if "username" in data and "password" in data and "firstname" in data and "lastname" in data:
            if not self.api.is_user_exists(data["username"]):
                self.api.create_user(data["username"], data["password"], data["firstname"], data["lastname"])
                return json({"Status":"OK"})
            return json({"Status":"User is already created"})
        return json({"Status":"Incorrect data: username, password, firstname, lastname"})

    async def method_patch(self, request: Request, body: dict) -> BaseHTTPResponse:
        if "token" not in request.cookies:
            return json({"Status": "Fail. Autorization is required"})
        if not self.api.is_token_valid(request.cookies["token"]):
            return json({"Status": "Fail. Token is invalid. Please, relogin"})

        data = body["DATA"]
        self.api.update_user_info(
            self.api.get_username_by_token(request.cookies["token"]),
            {
                "firstname": data["firstname"] if "firstname" in data else None,
                "lastname": data["lastname"] if "lastname" in data else None,
            }
        )
        return json({"Status": "OK"})
