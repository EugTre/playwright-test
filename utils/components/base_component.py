"""Base component class to inherit from."""
import logging

from abc import ABC, abstractmethod
from playwright.sync_api import Page


class BaseComponent(ABC):
    """Base component class."""
    def __init__(self, page: Page) -> None:
        self.page = page

    @property
    @abstractmethod
    def name(self):
        """Returns name of the component for loggign"""
        return "Unknown"

    def log(self, msg: str, *args, level: int = logging.INFO):
        """Logs message"""
        logging.log(level, f"[Component: {self.name}] {msg}", *args)

    @abstractmethod
    def should_be_visible(self):
        """Check component is visible"""
