from typing import Iterable
from sanic.request import Request
from sanic.response import BaseHTTPResponse, json
from api import Api


class EndpointBase:
    def __init__(self, api: Api, uri: str, methods: Iterable):
        self.uri = uri
        self.methods = methods
        self.api = api

    async def handler(self, request: Request) -> BaseHTTPResponse:
        body = {
            "ARGS": {key: value[0] for key, value in request.args.items()} if request.args is not None else {}, # NOTE used value[0] because the dict is kinda weird -> "key": ["value"]
            "DATA": dict(
                         **{key: value[0] for key, value in request.form.items()} if request.form is not None else {},
                         **{key: value[0] for key, value in request.json.items()} if "application/json" in request.content_type and request.json is not None else {},
                    )
        }
        return await self._method(request, body)

    async def _method(self, request: Request, body: dict):
        method = request.method.lower()
        func_name = "method_" + method
        if hasattr(self, func_name):
            func = getattr(self, func_name)
            return await func(request, body)
        return await self.method_not_impl(method)
    
    async def method_not_impl(self, method: str) -> BaseHTTPResponse:
        return json("Method " + method.upper() + " is not implemented", 500)