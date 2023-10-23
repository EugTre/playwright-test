"""Models of entites for Admin -> GeoZones page"""
from dataclasses import dataclass

from .table_entry import TableEntry


@dataclass
class CountryZoneEntity:
    """Represents Zone sub-enity of Geo Zone entity
    at Admin / Geo Zones page"""

    value: str | None
    zone_id: str | None = None
    city: str = ""


@dataclass
class GeozoneEntity(TableEntry):
    """Represents Geo Zone enity at Admin / Geo Zones page"""

    entity_id: str | None
    code: str = ""
    name: str = ""
    description: str = ""
    zones: list[CountryZoneEntity] | None = None

    def get_lookup_params(self):
        return {
            "id": self.entity_id,
            "name": self.name,
            "zones": len(self.zones)
        }
