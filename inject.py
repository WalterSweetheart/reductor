from configs import DatabaseConfig, ApiConfig, TransportConfig
from database import Database
from database.dumbdb import DumbDatabase
from api import Api
from api.simple_api import SimpleApi
from transport import Transport
from transport.sanic import SanicTransport


class Inject:
    Database: Database = DumbDatabase
    DatabaseConfig: DatabaseConfig = DatabaseConfig
    Api: Api = SimpleApi
    ApiConfig: ApiConfig = ApiConfig
    Transport: Transport = SanicTransport
    TransportConfig: TransportConfig = TransportConfig
