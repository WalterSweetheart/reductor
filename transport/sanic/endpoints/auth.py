from transport.sanic.endpoint_base import EndpointBase
from sanic.request import Request
from sanic.response import BaseHTTPResponse, json


class AuthEndpoint(EndpointBase):
    async def method_post(self, request: Request, body: dict) -> BaseHTTPResponse:
        if "token" in request.cookies and self.api.is_token_valid(request.cookies["token"]):
            return json({"Authorization": "Already"})
        data = body["DATA"]
        if "username" in data and "password" in data:
            if self.api.is_user_valid(data["username"], data["password"]):
                response = json({"Authorization": "Logined in"})
                response.cookies["token"] = self.api.generate_user_token(data["username"])
                return response
        return json({"Authorization": "Incorrect username or password"}, status=404)
