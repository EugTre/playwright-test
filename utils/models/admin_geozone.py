"""Models of entites for Admin -> GeoZones page"""
from dataclasses import dataclass

from .base_entity import BackOfficeEntity
from .entitiy_types import EntityType


@dataclass
class CountryZoneEntity:
    """Represents Zone sub-enity of Geo Zone entity
    at Admin / Geo Zones page"""

    value: str | None
    zone_id: str | None = None
    city: str = ""


@dataclass
class GeozoneEntity(BackOfficeEntity):
    """Represents Geo Zone enity at Admin / Geo Zones page"""
    code: str = ""
    name: str = ""
    description: str = ""
    zones: list[CountryZoneEntity] | None = None

    @property
    def entity_type(self) -> EntityType:
        """Type of the entity for handling via API"""
        return EntityType.GEOZONE

    def as_payload(self) -> dict:
        """Returns entity data in form of API request body"""
        output = {
            "code": self.code,
            "name": self.name,
            "description": self.description,
        }

        if not self.zones:
            return output

        for idx, zone in enumerate(self.zones):
            output[f"zones[new_{idx}][id]"] = ""
            output[f"zones[new_{idx}][country_code]"] = (
                zone.value if zone.value else ""
            )
            output[f"zones[new_{idx}][zone_code]"] = ""
            output[f"zones[new_{idx}][city]"] = zone.city

        return output

    def get_lookup_params(self) -> dict[str, str | int]:
        return {
            "id": self.entity_id,
            "name": self.name,
            "zones": len(self.zones)
        }
