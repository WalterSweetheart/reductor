from configs import TransportConfig
from api import Api


class Transport:
    def __init__(self, config: TransportConfig, api: Api):
        raise NotImplementedError
    
    def run(self):
        raise NotImplementedError