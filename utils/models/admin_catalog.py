"""Model for Product entity"""
import pathlib
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
    price: float
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

        price = f"{self.price:.2f}"
        if round(self.price) == self.price:
            price = f"{round(self.price)}"

        return {
            "id": self.entity_id,
            "name": self.name,
            "sku": self.sku,
            "price": price
        }

    def as_payload(self) -> dict[str, str]:
        # use "Fieldname": (None, _Value)
        empty = (None, "")
        payload = {
            "status": (None, 1),
            "date_valid_from": empty,
            "date_valid_to": empty,
            "name[en]": (None, self.name),
            "prices[USD]": (None, f"{self.price:.2f}"),
            "code": empty,
            "sku": (None, self.sku),
            "mpn": empty,
            "gtin": empty,
            "taric": empty,
            "manufacturer_id": empty,
            "supplier_id": empty,
            "keywords": empty,
            "short_description[en]": (None, self.short_desc),
            "description[en]": (None, self.full_desc),

            "head_title[en]": empty,
            "meta_description[en": empty,
            "technical_data[en]": empty,
            "new_attribute[group_id]": empty,
            "new_attribute[custom_value]": empty,

            "purchase_price": (None, 0,),
            "purchase_price_currency_code": (None, "USD"),
            "recommended_price": (None, "0.00"),
            "tax_class_id": empty,
            "gross_prices[USD]": (None, str(self.price)),
            "new_predefined_option[group_id]": empty,
            "new_predefined_option[custom_value]": empty,
            "new_user_input_option[group_id": empty,

            "quantity_min": (None, 0),
            "quantity_max": (None, 0),
            "quantity_step": (None, 0),
            "quantity_unit_id": (None, 1),
            "delivery_status_id": (None, 1),
            "sold_out_status_id": (None, 1),
            # sku
            "weight": (None, 0),
            "weight_class": (None, "kg"),
            "dim_x": (None, 0),
            "dim_y": (None, 0),
            "dim_z": (None, 0),
            "dim_class": (None, "cm"),
            "quantity": (None, str(self.quantity)),
            "quantity_adjustment": (None, str(self.quantity))
        }

        if not self.images:
            return payload

        # Add images
        for img in self.images:
            payload["new_images[]"] = (
                pathlib.Path(img).name,
                open(img, "rb"),
                "image/png"
            )

        return payload
