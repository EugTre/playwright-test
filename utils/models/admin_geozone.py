"""Models of entites for Admin -> GeoZones page"""
from dataclasses import dataclass


@dataclass
class CountryZoneEntity:
    """Represents Zone sub-enity of Geo Zone entity
    at Admin / Geo Zones page"""
    value: str | None
    zone_id: str | None = None
    city: str = ""


@dataclass
class GeozoneEntity:
    """Represents Geo Zone enity at Admin / Geo Zones page"""
    entity_id: str | None
    code: str = ""
    name: str = ""
    description: str = ""
    zones: list[CountryZoneEntity] | None = None
