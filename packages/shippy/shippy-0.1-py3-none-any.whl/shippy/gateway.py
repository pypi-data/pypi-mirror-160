


import importlib
from shippy.api import Api, ShipmentServices
from typing import Dict, List, Any
import enum

from shippy.shipment import Shipment

class Gateway:
    services: Dict[ShipmentServices, Api]
    def __init__(self):
        self.services = {}

    def register_api(self, api: Api):
        service: ShipmentServices
        for service in api.services:
            self.services[service] = api  # type: ignore

    def get_service_names(self):
        for service in self.services:
            yield service.value
    
    async def ship(self, shipment: Shipment, service: ShipmentServices):
        api = self.services[service]

        return await api.ship(shipment, service)