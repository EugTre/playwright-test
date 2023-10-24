"""Model for Product entity"""
from dataclasses import dataclass
from enum import Enum

from .entitiy_types import EntityType
from .base_entity import BackOfficeEntity


class ProductFormTab(Enum):
    """URL suffixes representing specifc tab
    at Create/Edit Product form"""

    GENERAL = "general"
    INFORMATION = "information"
    ATTRIBUTES = "attributes"
    PRICES = "prices"
    OPTIONS = "options"
    STOCK = "stock"


@dataclass(slots=True)
class ProductEntity(BackOfficeEntity):
    """Represents Product entity and contains it's fields"""

    name: str
    price: str | float
    sku: str

    short_desc: str | None = None
    full_desc: str | None = None
    quantity: int = 50
    images: list[str] | tuple[str] | None = None

    def __repr__(self) -> str:
        return (
            f"ProductEntity(entity_id={self.entity_id}, "
            f"name={self.name}, "
            f"price={self.price}, "
            f"sku={self.sku}, "
            f"short_desc={self.short_desc}, "
            f"full_desc={self.full_desc[:20]}, "
            f"quantity={self.quantity}, "
            f"images={self.images}"
            ")"
        )

    @property
    def entity_type(self) -> EntityType:
        return EntityType.PRODUCT

    def get_lookup_params(self) -> dict[str, str]:
        """Returns entry lookup params:
           - id
           - name
           - sku
           - price
        """
        return {
            "id": self.entity_id,
            "name": self.name,
            "sku": self.sku,
            "price": str(self.price)
        }

    def as_payload(self) -> dict[str, str]:
        return {}