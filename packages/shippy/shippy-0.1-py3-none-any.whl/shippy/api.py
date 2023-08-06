from dataclasses import dataclass
from urllib.parse import urljoin
import aiohttp
import enum

from shippy.shipment import Shipment
from typing import Dict

class ShipmentServices(str, enum.Enum):
    pass

class Api:
    services: enum.EnumMeta

    def __init__(self) -> None:
        pass

    async def ship(self, shipment: Shipment, service: ShipmentServices):
        raise NotImplemented
    
    async def get_label(self, shipment) -> bytes:
        raise NotImplemented