#!/bin/env python

from inject import Inject
from database import Database
from api import Api
from transport import Transport


class App:
    database: Database
    api: Api
    transport: Transport
    
    def __init__(self):
        self.database = Inject.Database(Inject.DatabaseConfig())
        self.api = Inject.Api(Inject.ApiConfig(), self.database)
        self.transport = Inject.Transport(Inject.TransportConfig(), self.api)
    
    def run(self):
        self.transport.run()


if __name__ == "__main__":
    App().run()
