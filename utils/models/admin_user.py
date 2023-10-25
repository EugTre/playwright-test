"""Entity for admin user"""
from dataclasses import dataclass
from datetime import datetime

from .base_entity import BackOfficeEntity
from .entitiy_types import EntityType


@dataclass
class UserEntity(BackOfficeEntity):
    """Admin user entity"""
    username: str
    password: str
    date_valid_from: str = "2023-01-01T00:00"
    date_valid_to: str = "2025-01-01T00:00"
    email: str = ""

    @property
    def entity_type(self) -> EntityType:
        """Returns EntityType of entity"""
        return EntityType.USER

    def as_payload(self) -> dict[str, str]:
        """Returns entity as dict of values ready to
        send to API"""
        return {
            "username": self.username,
            "password": self.password,
            "confirmed_password": self.password,
            "date_valid_from": self.date_valid_from,
            "date_valid_to": self.date_valid_to,
            "email": self.email,
            "status": "1"
        }

    def get_lookup_params(self):
        """Returns dictionary of params which may be
        used to find entity in the table views"""
        date_from = datetime.fromisoformat(self.date_valid_from) \
            .strftime("%b %d %Y %I:%M %p")
        date_to = datetime.fromisoformat(self.date_valid_to) \
            .strftime("%b %d %Y %I:%M %p")

        # Fix Py's date with leading zero by JS-like without one
        if date_from[4] == '0':
            date_from = f"{date_from[:4]}{date_from[5:]}"
        if date_to[4] == '0':
            date_to = f"{date_to[:4]}{date_to[5:]}"

        return {
            "id": self.entity_id,
            "username": self.username,
            "date_valid_from": date_from,
            "date_valid_to": date_to
        }
