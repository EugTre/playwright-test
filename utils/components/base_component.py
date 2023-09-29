"""Base component class to inherit from."""
from abc import ABC, abstractmethod
from playwright.sync_api import Page


class BaseComponent(ABC):
    """Base component class."""
    def __init__(self, page: Page) -> None:
        self.page = page

    @abstractmethod
    def should_be_visible(self):
        """Check component is visible"""
