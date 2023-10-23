"""Base class for entities that also represented in
table view"""
from abc import ABC, abstractmethod


class TableEntry(ABC):
    """Abstract class """

    @abstractmethod
    def get_lookup_params(self):
        """Returns dictionary of params which may be
        used to find entity in the table views"""
