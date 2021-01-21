from sanic.request import Request
from sanic.response import BaseHTTPResponse, json
from transport.sanic.endpoint_base import EndpointBase


class MsgEndpoint(EndpointBase):
    async def method_get(self, request: Request, body: dict) -> BaseHTTPResponse:
        if "token" not in request.cookies:
            return json({"Status": "Fail. Autorization is required"})
        if not self.api.is_token_valid(request.cookies["token"]):
            return json({"Status": "Fail. Token is invalid. Please, relogin"})
        messages = self.api.get_user_messages(self.api.get_username_by_token(request.cookies["token"]))
        out = []
        for message in messages:
            print(message)
            out.append({"sender": message["sender"], "message": message["message"], "sent_at": str(message["sent_at"])})
        return json(out)
    
    async def method_post(self, request: Request, body: dict) -> BaseHTTPResponse:
        if "token" not in request.cookies:
            return json({"Status": "Fail. Autorization is required"})
        if not self.api.is_token_valid(request.cookies["token"]):
            return json({"Status": "Fail. Token is invalid. Please, relogin"})
        
        data = body["DATA"]
        if "message" not in data or "reciever" not in data:
            return json({"Status": "Fail. Message or reciever is invalid"})
        if not self.api.is_user_exists(data["reciever"]):
            return json({"Status": "Fail. No such reciever"})
        self.api.send_message(
            sender=self.api.get_username_by_token(request.cookies["token"]),
            reciever=data["reciever"],
            message=data["message"],
        )
        return json({"Status": "OK"})

#    async def method_cheat(self, request: Request, body: dict) -> BaseHTTPResponse: #Sad. Custom methods doesn't work. :<
#        #NOTE WORKS ONLY WITH DUMBDB
#        return json({key: str(value) for key, value in self.api.database.database.items()})
