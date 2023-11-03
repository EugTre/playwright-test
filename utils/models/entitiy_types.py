from enum import StrEnum, auto
from dataclasses import dataclass


class EntityType(StrEnum):
    """Types of entities, used in helper functions
    during creation/deletion of the entities
    for tests"""

    USER = auto()
    GEOZONE = auto()
    PRODUCT = auto()


@dataclass
class EntityApiMapping:
    create_url: str
    delete_url: str
    create_as_url_form: bool = True
