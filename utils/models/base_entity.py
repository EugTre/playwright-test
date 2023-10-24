"""Base class for entities that also represented in
table view"""
from abc import ABC, abstractmethod
from dataclasses import dataclass

from .entitiy_types import EntityType


@dataclass
class BackOfficeEntity(ABC):
    """Protocol for entities that may be created
    and deleted via API call """
    entity_id: str | None

    @property
    @abstractmethod
    def entity_type(self) -> EntityType:
        """Returns EntityType of entity"""

    @abstractmethod
    def as_payload(self) -> dict[str, str]:
        """Returns entity as dict of values ready to
        send to API"""

    @abstractmethod
    def get_lookup_params(self):
        """Returns dictionary of params which may be
        used to find entity in the table views"""
