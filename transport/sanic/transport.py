from logging import debug
from transport import Transport
from configs import TransportConfig
from api import Api
import transport.sanic.endpoints
from sanic import Sanic
from .endpoints import get_binded_endpoints


class SanicTransport(Transport):
    def __init__(self, config: TransportConfig, api: Api):
        self.config = config
        self.api = api
        self.sanic = Sanic("Reductor")
        for endpoint in get_binded_endpoints(self.api):
            self.sanic.add_route(
                    handler=endpoint.handler,
                    uri=endpoint.uri,
                    methods=endpoint.methods,
                    strict_slashes=True,
            )
    
    def run(self):
        self.sanic.run(
                host=self.config.get_var("host") or "localhost",
                port=self.config.get_var("port") or 8000,
                debug=True,
        )
