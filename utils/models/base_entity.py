"""Base class for entities that also represented in
table view"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, MutableMapping

from .entitiy_types import EntityType


@dataclass
class BackOfficeEntity(ABC):
    """Abstract entity that:
    - may be created and deleted via API call
    - may be searched in table by some params"""
    entity_id: int | None

    @property
    @abstractmethod
    def entity_type(self) -> EntityType:
        """Returns EntityType of entity"""

    @abstractmethod
    def as_payload(
        self
    ) -> MutableMapping[str, Any]:
        """Returns entity as dict of values ready to
        send to API"""

    @abstractmethod
    def get_lookup_params(self):
        """Returns dictionary of params which may be
        used to find entity in the table views"""
