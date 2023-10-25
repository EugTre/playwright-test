from enum import StrEnum, auto


class EntityType(StrEnum):
    """Types of entities, used in helper functions
    during creation/deletion of the entities
    for tests"""

    USER = auto()
    GEOZONE = auto()
    PRODUCT = auto()
