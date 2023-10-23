"""Model for Product entity"""
from dataclasses import dataclass


@dataclass(slots=True)
class ProductEntity:
    """Represents Product entity and contains it's fields"""

    name: str
    price: float

    short_desc: str | None = None
    full_desc: str | None = None
    quantity: int = 50
    images: list[str] | tuple[str] | None = None
    product_id: str | None = None
