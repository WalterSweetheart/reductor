from transport.sanic.endpoint_base import EndpointBase
from sanic.request import Request
from sanic.response import BaseHTTPResponse, json


class UserEndpoint(EndpointBase):
    @EndpointBase.authorization_required
    async def method_get(self, request: Request, body: dict) -> BaseHTTPResponse:
        userinfo = self.api.get_user_info(self.api.get_username_by_token(request.cookies["token"]))
        return json({"username": userinfo["username"], "firstname": userinfo["firstname"], "created_at": str(userinfo["created_at"])})

    async def method_post(self, request: Request, body: dict) -> BaseHTTPResponse:
        data = body["DATA"]
        if "username" in data and "password" in data and "firstname" in data and "lastname" in data:
            if not self.api.is_user_exists(data["username"]):
                self.api.create_user(data["username"], data["password"], data["firstname"], data["lastname"])
                return json({"Status":"OK"}, status=201)
            return json({"Status":"User is already created"})
        return json({"Status":"Incorrect data: username, password, firstname, lastname"}, status=409)

    @EndpointBase.authorization_required
    async def method_patch(self, request: Request, body: dict) -> BaseHTTPResponse:
        data = body["DATA"]
        self.api.update_user_info(
            self.api.get_username_by_token(request.cookies["token"]),
            {
                "firstname": data.get("firstname"),
                "lastname": data.get("lastname"),
            }
        )
        return json({"Status": "OK"})
